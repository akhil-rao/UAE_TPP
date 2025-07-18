import streamlit as st
import pandas as pd

def run():
    st.title("📊 Customer 360 View – Multi-Bank Intelligence")

    # Load customer profile summary data
    @st.cache_data
    def load_data():
        return pd.read_csv("data/client_profile_summary.csv")

    df = load_data()

    # --- Main Pane Filters ---
    with st.expander("🔎 Filter Clients"):
        col1, col2, col3 = st.columns(3)

        with col1:
            client_names = sorted(df["Client Name"].unique())
            selected_client = st.multiselect("Select Client(s)", client_names, default=client_names)

        with col2:
            advisor_options = sorted(df["AI Recommendation"].unique())
            selected_advice = st.multiselect("AI Recommendation", advisor_options, default=advisor_options)

        with col3:
            banks = sorted(df["Bank"].unique())
            selected_banks = st.multiselect("Bank(s)", banks, default=banks)

    # Apply Filters
    filtered_df = df[
        (df["Client Name"].isin(selected_client)) &
        (df["AI Recommendation"].isin(selected_advice)) &
        (df["Bank"].isin(selected_banks))
    ]

    st.markdown(f"Showing **{len(filtered_df)}** bank records for selected clients.")
    st.dataframe(filtered_df, use_container_width=True)

    # --- Summary Section ---
    st.markdown("---")
    st.subheader("📌 Summary Insights (Aggregated by Client + Recommendation)")

    # Check for required columns
    required_cols = ["Client Name", "AI Recommendation", "Account Balance", "Loan Amount", "Monthly Income", "FX Transactions"]
    missing_cols = [col for col in required_cols if col not in filtered_df.columns]

    if missing_cols:
        st.warning(f"Cannot generate summary. Missing columns: {', '.join(missing_cols)}")
    else:
        grouped = filtered_df.groupby(["Client Name", "AI Recommendation"]).agg({
            "Account Balance": "sum",
            "Loan Amount": "sum",
            "Monthly Income": "mean",
            "FX Transactions": "sum"
        }).reset_index()

        st.dataframe(grouped.style.format({
            "Account Balance": "₹{:,.2f}",
            "Loan Amount": "₹{:,.2f}",
            "Monthly Income": "₹{:,.2f}",
            "FX Transactions": "{:.0f}"
        }), use_container_width=True)
