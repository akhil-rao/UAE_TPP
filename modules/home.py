import streamlit as st

def run_home():
    st.set_page_config(page_title="UAE TPP – Co-Pilot Modules", layout="wide")
    st.title("🏠 UAE TPP – Co-Pilot Modules")

    # Sidebar manual navigation
    st.sidebar.title("🧭 Navigation")
    selected_module = st.sidebar.selectbox("Choose a module", [
        "Home",
        "Customer 360 View"
        # Add others here if needed
    ])

    if selected_module == "Customer 360 View":
        # Dynamically run the customer_360 module
        from modules import customer_360
        customer_360.run()
        return  # Stop further execution if another module is loaded

    # If 'Home' is selected, show the module cards
    modules = [
        {"icon": "🧠", "title": "RM Copilot Chatbot", "desc": "Intelligent assistant for RMs with risk scoring and next-best actions"},
        {"icon": "🚘", "title": "Embedded Payments Agent", "desc": "Vehicle-aware contextual payments and insurance agent"},
        {"icon": "💱", "title": "FX Remittance Agent", "desc": "Suggests optimal remittance timing and provider options"},
        {"icon": "🚨", "title": "AML Alert Dashboard", "desc": "Visual risk analytics for high-risk corridors"},
        {"icon": "🧪", "title": "Nebras API Mock", "desc": "Simulated AISP data for accounts and transactions"},
    ]

    for mod in modules:
        st.markdown(f"### {mod['icon']} {mod['title']}")
        st.markdown(f"*{mod['desc']}*")
        st.markdown("---")
