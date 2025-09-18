import streamlit as st
import pandas as pd

def run_wealth_copilot():
    st.title(" Wealth Manager Copilot")

    # Realistic clients
    clients = [
        {"name": "Fatima Al Mansouri", "aum": 4.2, "income": 820, "risk": "Low", "risk_delta": "-1"},
        {"name": "Omar Al Fardan", "aum": 6.8, "income": 1200, "risk": "Medium", "risk_delta": "0"},
        {"name": "Salim Khan", "aum": 3.1, "income": 460, "risk": "High", "risk_delta": "+1"},
        {"name": "Laila Hassan", "aum": 2.7, "income": 510, "risk": "Medium", "risk_delta": "0"},
        {"name": "Yousef Al Qasimi", "aum": 7.5, "income": 1500, "risk": "Low", "risk_delta": "-2"},
        {"name": "Zara Noor", "aum": 5.9, "income": 910, "risk": "Medium", "risk_delta": "+1"},
        {"name": "Ahmed bin Zayed", "aum": 10.2, "income": 2000, "risk": "Low", "risk_delta": "-1"},
        {"name": "Noor Al Shamsi", "aum": 3.8, "income": 640, "risk": "High", "risk_delta": "+2"},
        {"name": "Khalid Al Mazrouei", "aum": 9.3, "income": 1300, "risk": "Low", "risk_delta": "-1"},
        {"name": "Dana Al Suwaidi", "aum": 4.6, "income": 760, "risk": "Medium", "risk_delta": "0"}
    ]

    client_names = [c["name"] for c in clients]
    selected_name = st.selectbox("Select Customer", client_names)
    client = next(c for c in clients if c["name"] == selected_name)

    st.markdown("### 🧾 Client Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total AUM", f"AED {client['aum']:.1f}M")
    col2.metric("Annual Income", f"AED {client['income']}K")
    col3.metric("Risk Score", client["risk"], delta=client["risk_delta"])

    st.markdown("---")
    st.markdown("### 🚗 Car Assets")
    car_data = pd.DataFrame({
        "Car": ["Land Cruiser", "Range Rover", "Ferrari", "BMW 7 Series"],
        "Year": [2023, 2022, 2024, 2025],
        "Fuel Type": ["Petrol", "Diesel", "Petrol", "EV"],
        "Estimated Value (AED)": [310000, 420000, 920000, 510000]
    })
    st.dataframe(car_data, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🧮 AI Advisor Mode – Tailored by Risk Profile")
    with st.expander("💡 See AI-Powered Recommendations"):

        if client["risk"] == "Low":
            st.markdown("- Maintain diversified equity exposure, consider fixed income for stability.")
            st.markdown("- Explore long-term retirement planning and estate structuring.")
            st.markdown("- Review insurance cover to match luxury asset growth.")
        elif client["risk"] == "Medium":
            st.markdown("- Increase allocation to bonds or market-neutral strategies.")
            st.markdown("- Revisit FX exposure across remittance and investment flows.")
            st.markdown("- Recommend partial hedging against rate volatility.")
        elif client["risk"] == "High":
            st.markdown("- Reduce exposure to volatile instruments (crypto, small caps).")
            st.markdown("- Recommend immediate portfolio rebalancing.")
            st.markdown("- Suggest automated alerts and RM check-ins every 2 weeks.")

    st.markdown("---")
    st.markdown("### 📈 Portfolio Allocation (Mock)")
    st.progress(70, text="Equities")
    st.progress(20, text="Fixed Income")
    st.progress(10, text="Cash & Others")

    st.markdown("### ✅ Risk Factors Used in Score")
    st.markdown("""
    - Debt-to-Income Ratio: 27%
    - Investment Volatility: Low
    - Insurance Coverage: Partial
    - Number of High-Value Assets: 4
    - Last RM Review: 45 days ago
    """)
