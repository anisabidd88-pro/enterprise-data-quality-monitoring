
import pandas as pd
from imputer import Imputer
from alerts import maybe_alert
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

def load_sources():
    sources = {}
    sources['mysql_customers'] = pd.read_csv(DATA_DIR / "mysql_customers.csv")
    sources['postgres_orders'] = pd.read_csv(DATA_DIR / "postgres_orders.csv")
    sources['api_events'] = pd.read_csv(DATA_DIR / "api_saas_events.csv")
    sources['saas_contacts'] = pd.read_csv(DATA_DIR / "saas_contacts.csv")
    return sources

def run_dbt_like_tests(sources):
    tests = []
    tests.append({
        "source":"mysql_customers",
        "test":"primary_key_unique:customer_id",
        "passed": bool(sources['mysql_customers']['customer_id'].is_unique)
    })
    tests.append({
        "source":"postgres_orders",
        "test":"no_null:order_id,amount",
        "passed": not sources['postgres_orders'][['order_id','amount']].isnull().any().any()
    })
    orders = sources['postgres_orders']
    cust_ids = set(sources['mysql_customers']['customer_id'].tolist())
    missing = orders[~orders['customer_id'].isin(cust_ids)]
    tests.append({
        "source":"postgres_orders",
        "test":"referrer_integrity:customer_id",
        "passed": missing.empty,
        "details": missing.to_dict(orient='records')[:5]
    })
    return pd.DataFrame(tests)

def compute_quality_scores(sources):
    scores = []
    cust = sources['mysql_customers']
    completeness = 1 - (cust[['email','age','city']].isnull().mean().mean())
    pk_unique = float(cust['customer_id'].is_unique)
    invalid_emails = cust['email'].str.contains("@").fillna(False).mean()
    score = (completeness*0.5 + pk_unique*0.2 + invalid_emails*0.3)
    scores.append({"source":"mysql_customers","score":round(score*100,2)})
    orders = sources['postgres_orders']
    zero_amount = (orders['amount']<=0).mean()
    missing_ref = (~orders['customer_id'].isin(cust['customer_id'])).mean()
    score_o = max(0, 1 - (zero_amount*0.6 + missing_ref*0.4))
    scores.append({"source":"postgres_orders","score":round(score_o*100,2)})
    events = sources['api_events']
    missing_ts = events['event_time'].isnull().mean()
    scores.append({"source":"api_events","score":round((1-missing_ts)*100,2)})
    contacts = sources['saas_contacts']
    bad_email = ~contacts['email'].str.contains("@").fillna(False)
    scores.append({"source":"saas_contacts","score":round((1-bad_email.mean())*100,2)})
    return pd.DataFrame(scores)

def generate_reports(scores, tests):
    now = datetime.utcnow().isoformat()
    out_csv = REPORTS_DIR / "data_quality_report.csv"
    rows=[]
    for s in scores.to_dict(orient='records'):
        src=s['source']
        sc=s['score']
        tsts=[t for t in tests.to_dict(orient='records') if t['source']==src]
        if tsts:
            for t in tsts:
                rows.append({"source":src,"score":sc,"test":t['test'],"passed":t['passed']})
        else:
            rows.append({"source":src,"score":sc,"test":None,"passed":None})
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    return out_csv

def main():
    print("Loading sources...")
    sources = load_sources()
    print("Running tests...")
    tests = run_dbt_like_tests(sources)
    print("Computing scores...")
    scores = compute_quality_scores(sources)
    print("Imputing missing values (ML)...")
    imputer = Imputer()
    cust = sources['mysql_customers']
    cust_imputed = imputer.impute_dataframe(cust, target_cols=['age'])
    cust_imputed.to_csv("reports/customers_imputed.csv", index=False)
    out = generate_reports(scores, tests)
    print("Report written to", out)
    low = scores[scores['score'] < 80]
    if not low.empty:
        maybe_alert(low.to_dict(orient='records'))
    print("Done.")

if __name__ == '__main__':
    main()
