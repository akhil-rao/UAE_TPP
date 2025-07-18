import streamlit as st
import pandas as pd

def run():
    st.set_page_config(page_title="Customer 360 View", layout="wide")
    st.title("📊 Customer 360 View – RM Dashboard (Ajman Bank)")

    @st.cache_data
    def load_data():
        return pd.read_csv("data/client_profile_summary.csv")

    df = load_data()
    ajman_bank = "Ajman Bank"

    # --- MAIN FILTER ---
    st.markdown("### 🔎 Filter by UAE ID")
    uae_ids = sorted(df["UAE ID"].unique())
    selected_uae_id = st.selectbox("Select UAE ID", uae_ids)

    client_df = df[df["UAE ID"] == selected_uae_id]
    if client_df.empty:
        st.warning("No records found.")
        return

    client_name = client_df["Client Name"].iloc[0]
    st.markdown(f"#### 👤 Client: `{client_name}` | UAE ID: `{selected_uae_id}`")

    # --- RELATIONSHIP OVERVIEW ---
    st.subheader("🏦 Relationship Summary Across Banks")
    for bank in sorted(client_df["Bank"].unique()):
        products = ", ".join(client_df[client_df["Bank"] == bank]["Products Used"].unique())
        tag = "🟢" if bank == ajman_bank else "🔵"
        st.markdown(f"- {tag} **{bank}**: {products}")

    # --- SMART ALERTS ---
    st.subheader("🚨 Smart Product Alerts for Ajman Bank")
    ajman_products = client_df[client_df["Bank"] == ajman_bank]["Products Used"].unique()
    other_bank_df = client_df[client_df["Bank"] != ajman_bank]
    other_products = other_bank_df["Products Used"].unique()

    alerts = []
    for prod in other_products:
        if prod not in ajman_products:
            # find which bank offers it
            prod_banks = other_bank_df[other_bank_df["Products Used"] == prod]["Bank"].unique()
            bank_list = ", ".join(prod_banks)
            alerts.append(f"❗ Client has **{prod}** with {bank_list} but not with Ajman Bank.")

    if alerts:
        for a in alerts:
            st.markdown(f"- {a}")
    else:
        st.success("✅ Ajman Bank already offers all products the client holds elsewhere.")

    # --- AI RECOMMENDATIONS ---
    st.subheader("🤖 AI Cross-Sell Suggestions for Ajman Bank")

    for reco in client_df["AI Recommendation"].unique():
        already_offered = any(prod in reco for prod in ajman_products)
        icon = "✅" if already_offered else "💡"
        color = "green" if already_offered else "orange"
        st.markdown(f"- <span style='color:{color}'>{icon} {reco}</span>", unsafe_allow_html=True)

    # --- FULL ACCOUNT VIEW ---
    st.markdown("---")
    st.subheader("📋 Full Account Overview (All Banks)")
    st.dataframe(client_df, use_container_width=True)

    # --- SUMMARY BY BANK ---
    st.subheader("📌 Financial Summary by Bank")
    summary = client_df.groupby("Bank").agg({
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
