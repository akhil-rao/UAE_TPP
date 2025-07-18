import streamlit as st

def run_home():
    st.title("🏠 UAE TPP – Co-Pilot Modules")
    st.markdown("Welcome to the UAE TPP Sandbox. Below are the available agentic AI modules:")

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
