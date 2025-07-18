import streamlit as st
import pandas as pd

def run():
    # Set page config
    st.set_page_config(page_title="Customer 360 View", layout="wide")
    st.title("📊 Customer 360 View – Multi-Bank Intelligence")

    # Load data
    @st.cache_data
    def load_data():
        return pd.read_csv("data/client_profile_summary.csv")

    df = load_data()

    # --- Sidebar Filter by UAE ID ---
    st.sidebar.header("🔎 Filter by UAE ID")
    uae_ids = sorted(df["UAE ID"].unique())
    selected_uae_id = st.sidebar.selectbox("Select UAE ID", uae_ids)

    # Filter data for selected UAE ID
    filtered_df = df[df["UAE ID"] == selected_uae_id]

    if filtered_df.empty:
        st.warning("No records found for the selected UAE ID.")
        return

    # Extract client name
    client_name = filtered_df["Client Name"].iloc[0]

    # --- Relationship Summary ---
    st.markdown(f"### 🧠 Relationship Summary for `{client_name}` ({selected_uae_id})")

    for bank in filtered_df["Bank"].unique():
        bank_data = filtered_df[filtered_df["Bank"] == bank]
        products = ", ".join(bank_data["Products Used"].unique())
        st.markdown(f"- **{bank}**: {products}")

    # --- AI Recommendations ---
    st.markdown("### ✅ AI Recommendations")
    for reco in filtered_df["AI Recommendation"].unique():
        st.markdown(f"- {reco}")

    st.markdown("---")

    # --- Full Account Overview ---
    st.subheader("📋 Full Account Overview")
    st.dataframe(filtered_df, use_container_width=True)

    # --- Summary by Bank ---
    st.markdown("### 📌 Summary by Bank")
    summary = filtered_df.groupby("Bank").agg({
        "Account Balance": "sum",
        "Loan Amount": "sum",
        "Monthly Income": "mean",
        "FX Transactions": "sum"
    }).reset_index()

    st.dataframe(summary.style.format({
        "Account Balance": "₹{:,.2f}",
        "Loan Amount": "₹{:,.2f}",
        "Monthly Income": "₹{:,.2f}",
        "FX Transactions": "{:.0f}"
    }), use_container_width=True)
