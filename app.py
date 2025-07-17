import streamlit as st
from modules.rm_copilot import run_copilot
from modules.fx_remittance_advisor import run_fx_advisor

st.set_page_config(page_title="PaymentLabs.AI Demo", layout="wide")
st.title("💡 PaymentLabs.AI - AI-Powered Copilot")

menu = st.sidebar.radio("Select Module", ["RM Copilot", "FX Remittance Advisor"])

if menu == "RM Copilot":
    run_copilot()
elif menu == "FX Remittance Advisor":
    run_fx_advisor()
