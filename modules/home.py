import streamlit as st

def run_home():
    st.set_page_config(page_title="UAE TPP – Co-Pilot Modules", layout="wide")
    st.title("🏠 UAE TPP – Co-Pilot Modules")

    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    st.sidebar.page_link("modules/customer_360.py", label="Customer 360 View")

    modules = [
        {"icon": "🧠", "title": "RM Copilot Chatbot", "desc": "Intelligent assistant for RMs with risk scoring and next-best actions"},
        {"icon": "🚘", "title": "Embedded Payments Agent", "desc": "Vehicle-aware contextual payments and insurance agent"},
        {"icon": "💱", "title": "FX Remittance Agent", "desc": "Suggests optimal remittance timing and provider options"},
        {"icon": "🚨", "title": "AML Alert Dashboard", "desc": "Visual risk analytics for high-risk corridors"},
        {"icon": "🧪", "title": "Nebras API Mock", "desc": "Simulated AISP data for accounts and transactions"}
    ]

    for mod in modules:
        st.markdown(f"### {mod['icon']} {mod['title']}")
        st.markdown(f"*{mod['desc']}*")
        st.markdown("---")
