import streamlit as st
import pandas as pd

def run_aml_alerts():
    st.header("🚨 AML & Risk Alert Dashboard")
    df = pd.read_csv("data/aml_alerts.csv")
    st.bar_chart(df.set_index("Country"))
    st.warning("3 high-risk corridors detected. Review recommended before PISP authorization.")
