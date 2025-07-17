import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def run_fx_agent():
    st.header("💱 FX Remittance AI Agent")

    st.subheader("FX Rate Trend (AED to INR)")
    df = pd.read_csv("data/fx_trends.csv")
    st.line_chart(df.set_index("Date"))

    st.subheader("Remittance Recommendation")
    amount = st.number_input("Monthly Remittance Amount (AED)", value=1000)
    st.write("Today's AED/INR rate: 23.10")
    st.write("✅ Better than last month. Consider remitting today.")

    st.subheader("Provider Comparison")
    providers = {"Wise": 18.5, "Lulu Exchange": 22.0, "Mashreq": 21.7}
    st.bar_chart(pd.Series(providers))
