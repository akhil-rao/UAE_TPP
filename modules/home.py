import streamlit as st

def run_home():
    st.set_page_config(page_title="UAE TPP – Co-Pilot Modules", layout="wide")
    st.title("🏠 UAE TPP – Co-Pilot Modules")

    modules = [
        {
            "icon": "🧠",
            "title": "RM Copilot Chatbot",
            "desc": "Intelligent assistant for RMs with risk scoring and next-best actions",
            "module": "rm_copilot"
        },
        {
            "icon": "🚘",
            "title": "Embedded Payments Agent",
            "desc": "Vehicle-aware contextual payments and insurance agent",
            "module": "embedded_payments"
        },
        {
            "icon": "💱",
            "title": "FX Remittance Agent",
            "desc": "Suggests optimal remittance timing and provider options",
            "module": "fx_remittance"
        },
        {
            "icon": "🚨",
            "title": "AML Alert Dashboard",
            "desc": "Visual risk analytics for high-risk corridors",
            "module": "aml_alert"
        },
        {
            "icon": "🧪",
            "title": "Nebras API Mock",
            "desc": "Simulated AISP data for accounts and transactions",
            "module": "nebras_api"
        },
        {
            "icon": "📊",
            "title": "Customer 360 View",
            "desc": "Multi-bank intelligence with AI recommendations and financial insights",
            "module": "customer_360"
        }
    ]

    for mod in modules:
        st.markdown(f"### {mod['icon']} {mod['title']}")
        st.markdown(f"*{mod['desc']}*")
        if st.button(f"Open {mod['title']}"):
            # Dynamically run the selected module
            from modules import customer_360
            customer_360.run()
            st.stop()  # Stop further execution
        st.markdown("---")
