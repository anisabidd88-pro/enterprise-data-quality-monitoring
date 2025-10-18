
from dash import Dash, html, dcc
import pandas as pd
from pathlib import Path
import webbrowser
import threading

REPORT = Path(__file__).parents[1] / "reports" / "data_quality_report.csv"

app = Dash(__name__)

def serve_layout():
    if REPORT.exists():
        df = pd.read_csv(REPORT)
        scores = df.groupby('source')['score'].first().reset_index()
        return html.Div([
            html.H1("Data Quality — Dash (Demo)"),
            dcc.Graph(
                figure={
                    "data":[{"x":scores['source'].tolist(),"y":scores['score'].tolist(),"type":"bar"}],
                    "layout":{"title":"Quality Scores"}
                }
            ),
            html.H2("Tests"),
            html.Pre(df.to_csv(index=False))
        ])
    else:
        return html.Div([html.H3("Run pipeline first (python pipeline.py)")])

app.layout = serve_layout

if __name__=='__main__':
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:8050")).start()
    app.run_server(debug=False)
