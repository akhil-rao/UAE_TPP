import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Customer 360 View", layout="wide")
st.title("📊 Customer 360 View – Multi-Bank Intelligence")

# Load the customer dataset
@st.cache_data
def load_data():
    return pd.read_csv("modules/data/customer_360_demo.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔎 Filter Clients")

client_names = sorted(df["Client Name"].unique())
selected_client = st.sidebar.multiselect("Select Client(s)", client_names, default=client_names)

advisor_options = sorted(df["AI Advisor Output"].unique())
selected_advice = st.sidebar.multiselect("AI Advisor Output", advisor_options, default=advisor_options)

banks = sorted(df["Bank"].unique())
selected_banks = st.sidebar.multiselect("Bank(s)", banks, default=banks)

# Apply filters
filtered_df = df[
    (df["Client Name"].isin(selected_client)) &
    (df["AI Advisor Output"].isin(selected_advice)) &
    (df["Bank"].isin(selected_banks))
]

# Display filtered table
st.markdown(f"Showing **{len(filtered_df)}** bank records for selected clients.")
st.dataframe(filtered_df, use_container_width=True)

# Summary insights
st.markdown("---")
st.subheader("📌 Summary Insights")

grouped = filtered_df.groupby(["Client Name", "AI Advisor Output"]).agg({
    "Account Balance": "sum",
    "Loan Amount": "sum",
    "Monthly Income": "mean",
    "Credit Score": "mean",
    "FX Transactions": "sum"
}).reset_index()

st.dataframe(grouped.style.format({
    "Account Balance": "₹{:,.2f}",
    "Loan Amount": "₹{:,.2f}",
    "Monthly Income": "₹{:,.2f}",
    "Credit Score": "{:.0f}",
    "FX Transactions": "{:.0f}"
}), use_container_width=True)
