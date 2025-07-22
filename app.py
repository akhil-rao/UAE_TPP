import streamlit as st 
from modules.home import run_home
from modules.rm_copilot import run_rm_copilot
from modules.embedded_payments import run_embedded_payments
from modules.fx_remittance_agent import run_fx_agent
from modules.aml_alerts import run_aml_alerts
from modules.customer_360 import run as run_customer_360
from modules.wealth_manager_streamlit import run_wealth_copilot  # ✅ NEW

st.set_page_config(page_title="UAE TPP Co-Pilot Demo", layout="wide")

st.sidebar.title("UAE TPP Modules")
option = st.sidebar.radio("Choose a Module", [
    "Home",
    "RM Copilot",
    "Embedded Payments Agent",
    "FX Remittance Agent",
    "AML Alert Dashboard",
    "Customer 360 View",
    "Wealth Manager Copilot (Streamlit)"  # ✅ NEW
])

if option == "Home":
    run_home()
elif option == "RM Copilot":
    run_rm_copilot()
elif option == "Embedded Payments Agent":
    run_embedded_payments()
elif option == "FX Remittance Agent":
    run_fx_agent()
elif option == "AML Alert Dashboard":
    run_aml_alerts()
elif option == "Customer 360 View":
    run_customer_360()
elif option == "Wealth Manager Copilot (Streamlit)":  # ✅ NEW
    run_wealth_copilot()
