import streamlit as st
import pandas as pd

def run():
    st.set_page_config(page_title="Customer 360 View", layout="wide")
    st.title("📊 Customer 360 View – Multi-Bank Intelligence")

    # Load client profile summary
    @st.cache_data
    def load_data():
        return pd.read_csv("data/client_profile_summary.csv")

    df = load_data()

    # --- Filter by UAE ID ---
    with st.expander("🔍 Filter by UAE ID", expanded=True):
        uae_ids = sorted(df["UAE ID"].unique())
        selected_uae_id = st.selectbox("Select UAE ID", uae_ids)
        selected_df = df[df["UAE ID"] == selected_uae_id]
        client_name = selected_df["Client Name"].iloc[0]
        st.markdown(f"**👤 Client:** {client_name} | **UAE ID:** {selected_uae_id}")

    st.markdown("---")

    # --- Relationship Summary Table ---
    st.subheader("🏦 Relationship Summary Across Banks")
    relationship_table = (
        selected_df.groupby("Bank")["Products Used"]
        .apply(lambda x: ", ".join(sorted(x.unique())))
        .reset_index()
        .rename(columns={"Products Used": "Products Held"})
    )
    st.dataframe(relationship_table, use_container_width=True)

    # --- Smart Alerts for Ajman Bank ---
    st.subheader("🚨 Smart Product Alerts for Ajman Bank")
    ajman_products = set(selected_df[selected_df["Bank"] == "Ajman Bank"]["Products Used"].unique())

    alert_rows = []
    for bank in relationship_table["Bank"].unique():
        if bank == "Ajman Bank":
            continue
        bank_products = set(selected_df[selected_df["Bank"] == bank]["Products Used"].unique())
        missing_products = sorted(bank_products - ajman_products)
        if missing_products:
            alert_rows.append({
                "Bank": bank,
                "Missing Products (Not in Ajman Bank)": ", ".join(missing_products)
            })

    if alert_rows:
        alert_df = pd.DataFrame(alert_rows)
        st.dataframe(alert_df, use_container_width=True)
    else:
        st.success("✅ No missing products. Client already has all products with Ajman Bank.")

    # --- Full Record View (Optional) ---
    with st.expander("🧾 View Raw Data for This Client"):
        st.dataframe(selected_df, use_container_width=True)
