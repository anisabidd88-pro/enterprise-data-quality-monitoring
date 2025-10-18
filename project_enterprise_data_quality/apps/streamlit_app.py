
import streamlit as st
import pandas as pd
from pathlib import Path

REPORT = Path(__file__).parents[1] / "reports" / "data_quality_report.csv"

st.set_page_config(page_title="Data Quality Dashboard", layout="wide")
st.title("Enterprise Data Quality Monitoring")

if REPORT.exists():
    df = pd.read_csv(REPORT)
    st.subheader("Scores by source")
    scores = df.groupby('source')['score'].first().reset_index()
    st.dataframe(scores)
    st.bar_chart(scores.set_index('source')['score'])
    st.subheader("Tests")
    st.dataframe(df[['source','test','passed']])
else:
    st.warning("Run pipeline first (python pipeline.py) to generate reports.")
