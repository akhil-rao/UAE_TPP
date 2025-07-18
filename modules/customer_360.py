import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Customer 360 View", layout="wide")
st.title("📊 Customer 360 View – Multi-Bank Intelligence")

# Load customer profile summary data from root-level data folder
@st.cache_data
def load_data():
    return pd.read_csv("data/client_profile_summary.csv")

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔎 Filter Clients")

client_names = sorted(df["Client Name"].unique())
selected_client = st.sidebar.multiselect("Select Client(s)", client_names, default=client_names)

advisor_options = sorted(df["AI Recommendation"].unique())
selected_advice = st.sidebar.multiselect("AI Recommendation", advisor_options, default=advisor_options)

banks = sorted(df["Bank"].unique())
selected_banks = st.sidebar.multiselect("Bank(s)", banks, default=banks)

# --- Apply Filters ---
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

grouped = filtered_df.groupby(["Client Name", "AI Recommendation"]).agg({
    "Account Balance": "sum",
    "Loan Amount": "sum",
    "Monthly Income": "mean",
    "Credit Score": "mean" if "Credit Score" in df.columns else "mean",
    "FX Transactions": "sum"
}).reset_index()

# Format numbers
st.dataframe(grouped.style.format({
    "Account Balance": "₹{:,.2f}",
    "Loan Amount": "₹{:,.2f}",
    "Monthly Income": "₹{:,.2f}",
    "Credit Score": "{:.0f}" if "Credit Score" in df.columns else "{:.0f}",
    "FX Transactions": "{:.0f}"
}), use_container_width=True)
