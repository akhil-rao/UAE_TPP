import streamlit as st
import pandas as pd

def run():
    st.set_page_config(page_title="Customer 360 View", layout="wide")
    st.title("📊 Customer 360 View – Multi-Bank Intelligence")

    # Load client profile data
    @st.cache_data
    def load_data():
        return pd.read_csv("data/client_profile_summary.csv")

    df = load_data()

    # --- Filter by UAE ID ---
    st.markdown("### 🔍 Filter by Client UAE ID")
    uae_ids = sorted(df["UAE ID"].unique())
    selected_id = st.selectbox("Select UAE ID", uae_ids)

    client_df = df[df["UAE ID"] == selected_id]
    client_name = client_df["Client Name"].iloc[0]

    st.markdown(f"👤 **Client:** {client_name} &nbsp;&nbsp;|&nbsp;&nbsp; 🆔 **UAE ID:** {selected_id}")

    # --- Relationship Summary Across Banks ---
    st.markdown("### 🏦 Relationship Summary Across Banks")
    rel_summary = client_df.groupby("Bank")["Products Used"].apply(
        lambda x: ", ".join(sorted(x.unique()))
    ).reset_index().rename(columns={"Products Used": "Products Held"})
    st.dataframe(rel_summary, use_container_width=True)

    # --- AI Recommendation Summary ---
    st.markdown("### 🤖 AI Recommendation Summary")

    summary_df = client_df.groupby(["Client Name", "AI Recommendation"]).agg({
        "Account Balance": "sum",
        "Loan Amount": "sum",
        "Monthly Income": "mean",
        "FX Transactions": "sum"
    }).reset_index()

    st.dataframe(summary_df.style.format({
        "Account Balance": "₹{:,.2f}",
        "Loan Amount": "₹{:,.2f}",
        "Monthly Income": "₹{:,.2f}",
        "FX Transactions": "{:.0f}"
    }), use_container_width=True)

    # Optional raw view
    with st.expander("🔍 View All Bank Records for this Client"):
        st.dataframe(client_df, use_container_width=True)
