import streamlit as st
from modules.rm_copilot import run_rm_copilot
from modules.embedded_payments import run_embedded_payments
from modules.fx_remittance_agent import run_fx_agent

st.set_page_config(page_title="UAE TPP Co-Pilot Demo", layout="wide")
st.title("🤖 UAE TPP - Co-Pilot Modules")

option = st.sidebar.radio("Choose a Module", [
    "RM / Advisor Copilot",
    "Embedded Payments Agent",
    "FX Remittance Agent"
])

if option == "RM / Advisor Copilot":
    run_rm_copilot()
elif option == "Embedded Payments Agent":
    run_embedded_payments()
elif option == "FX Remittance Agent":
    run_fx_agent()

from modules.aml_alerts import run_aml_alerts
if option == "AML Alert Dashboard":
    run_aml_alerts()
