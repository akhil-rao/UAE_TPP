import streamlit as st
import pandas as pd
import random

def run_wealth_copilot():
    st.title("🧠 Wealth Manager Copilot")

    # Dummy customer selector
    customers = [f"Client {i:02d}" for i in range(1, 11)]
    selected_customer = st.selectbox("Select Customer", customers)

    st.markdown("### 🧾 Client Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total AUM", "AED 4.2M", "+2.5% MoM")
    col2.metric("Annual Income", "AED 820K")
    col3.metric("Risk Score", "Low", delta="-1")

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
    st.markdown("### 🧮 AI Advisor Insights")
    with st.expander("💡 See AI-Powered Recommendations"):
        st.markdown("- Suggest portfolio rebalance towards fixed income for capital preservation.")
        st.markdown("- Recommend insurance review: 3 uncovered luxury vehicles.")
        st.markdown("- Introduce green investment options aligned with EV ownership.")
        st.markdown("- Offer FX hedging for EUR-denominated assets.")

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

    st.success("This module is 100% Streamlit-native – no iframe or external React dependency.")
