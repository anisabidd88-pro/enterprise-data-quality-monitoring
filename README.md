# 🏢 Enterprise Data Quality Monitoring System

### 🔍 Overview
This project is a **complete enterprise-grade data quality monitoring system** designed to check, track, and continuously improve the quality of data across multiple company sources.  
It integrates multiple databases, APIs, and SaaS tools into a unified monitoring framework — giving visibility, correction, and alerts on data health in real time.

---

## 🚀 Key Features

- **Multi-Source Data Integration**
  - Collects data from:
    - MySQL  
    - PostgreSQL  
    - REST APIs  
    - SaaS platforms (HubSpot, Salesforce, etc.)

- **Automated Data Validation**
  - Detects missing values, duplicates, anomalies, and inconsistencies  
  - Includes a folder `/dbt_tests/` prepared for future **dbt tests** (you can add your own rules later)

- **Machine Learning Data Correction**
  - Uses ML-based imputation to estimate and replace missing or invalid values automatically  
  - Improves reliability and trust in your datasets

- **Interactive Dashboards**
  - Built using **Streamlit** and **Plotly Dash**  
  - Provides instant visual feedback on data quality and metrics

- **Alerting System**
  - Slack and Email alerts for low data quality or failed validation thresholds

- **Reports & Scoring**
  - Automatically generates reports and quality scores per source or table  
  - Helps Data Science and Product teams rely on clean, trusted data



## 🧠 How It Works

1. **Data Loading**
   - Reads data from multiple sources (SQL, API, CSV…).
2. **Validation**
   - Checks data integrity, consistency, and missing values.
3. **Correction**
   - Cleans data and predicts missing values using `imputer.py`.
4. **Scoring**
   - Calculates a "Data Quality Score" per table/source.
5. **Reporting**
   - Saves results to `/reports/data_quality_report.csv`.
6. **Visualization**
   - Dashboards show metrics in real time via Streamlit or Dash.
7. **Alerts**
   - Sends notifications when thresholds are not met.

---

## 🧾 Important Notes

> 🟡 The data inside `/data/` folder is **only sample data** for demonstration.  
> You can **replace it with your own company data** (from any source).  
>  
> The folder `/dbt_tests/` is **ready but optional** —  
> you can later add your **own dbt models and tests** if you want to integrate this project with dbt pipelines.

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

git clone https://github.com/yourusername/enterprise-data-quality.git
cd enterprise-data-quality
2️⃣ Create a virtual environment

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
3️⃣ Install required packages

pip install -r requirements.txt
4️⃣ Configure environment
Copy and edit the environment file:

cp .env.example .env
5️⃣ Run the pipeline

python pipeline.py
6️⃣ Launch the dashboards
Streamlit:

streamlit run apps/streamlit_app.py
Plotly Dash:

python apps/dash_app.py
📊 Example Output
Source	Table	Missing Values	Duplicates	Quality Score
MySQL	customers	3	1	96%
PostgreSQL	orders	0	0	100%
SaaS	contacts	2	0	93%
🔔 Alerts Example
⚠️ Slack Notification:
“Data Quality Alert: customers table dropped to 82% quality.”
📧 Email Alert:
Sent automatically when any table score < 70%.
🧩 Future Enhancements
Integrate Great Expectations or Soda SQL
Add dbt pipeline for transformation testing
Include advanced anomaly detection (IsolationForest, AutoEncoder)
Airflow or Prefect scheduling for automation
Connection to BI tools (Power BI, Tableau)
🧑‍💻 Author
Enterprise Data Quality Monitoring System
Developed with ❤️ using Python, Streamlit, and Plotly.
You are free to:
Replace sample data with your own
Extend dbt tests in /dbt_tests/
Upgrade validation logic as you wish
📜 License
MIT License © 2025

