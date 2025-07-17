import streamlit as st

def run_copilot():
    st.header("🧠 RM / Relationship Manager Copilot")

    name = st.text_input("Client Name")
    annual_income = st.number_input("Annual Income (AED)", min_value=0)
    risk_profile = st.selectbox("Risk Profile", ["Low", "Medium", "High"])
    interests = st.multiselect("Financial Interests", ["Credit Card", "Investment", "Insurance", "FX Remittance", "SME Loan"])

    if st.button("Generate Suggestions"):
        st.subheader("✅ Copilot Suggestions")
        st.write("Based on income and interests, we suggest:")
        if "Investment" in interests:
            st.write("- SmartPortfolio AI-managed fund")
        if "Insurance" in interests:
            st.write("- Family Takaful Plan with Maturity Bonus")
        if "FX Remittance" in interests:
            st.write("- RemitSmart FX Bundle with fee waiver")
