import streamlit as st
import pandas as pd

def run():
    st.set_page_config(page_title="Customer 360 View", layout="wide")
    st.title("📊 Customer 360 View – Unified with Lifestyle & AI")

    @st.cache_data
    def load_data():
        # Load lifestyle info
        lifestyle = pd.DataFrame([
            {"UAE ID": "784-1234-567890-1", "Client Name": "Fatima Al Mansouri", "Nationality": "UAE",
             "Property Location": "Dubai Marina", "Property Value": 3100000, "Utility Provider": "DEWA",
             "Monthly Utility Bill": 1450, "Medical Insurance": "None", "Credit Card Activity": "Air Tickets",
             "Car Type": "BMW 7 Series", "Car Year": 2023},
            {"UAE ID": "784-9876-543210-2", "Client Name": "Omar Al Fardan", "Nationality": "Expat",
             "Property Location": "Sharjah Al Khan", "Property Value": 1200000, "Utility Provider": "SEWA",
             "Monthly Utility Bill": 650, "Medical Insurance": "Yes (AXA)", "Credit Card Activity": "Online Shopping",
             "Car Type": "Toyota Prado", "Car Year": 2021},
            {"UAE ID": "784-2468-135790-3", "Client Name": "Salim Khan", "Nationality": "Expat",
             "Property Location": "Business Bay", "Property Value": 2150000, "Utility Provider": "DEWA",
             "Monthly Utility Bill": 980, "Medical Insurance": "None", "Credit Card Activity": "Air Tickets, Dining",
             "Car Type": "Tesla Model Y", "Car Year": 2024},
            {"UAE ID": "784-3698-147025-4", "Client Name": "Laila Hassan", "Nationality": "UAE",
             "Property Location": "Abu Dhabi Saadiyat", "Property Value": 5800000, "Utility Provider": "ADDC",
             "Monthly Utility Bill": 1950, "Medical Insurance": "Yes (Daman)", "Credit Card Activity": "Travel",
             "Car Type": "Range Rover", "Car Year": 2022}
        ])

        # Load multi-bank product usage
        df = pd.read_csv("data/multi_bank_profile.csv")  # Replace with your actual saved path
        return df, lifestyle

    df_core, df_life = load_data()

    uae_ids = sorted(df_life["UAE ID"].unique())
    selected_id = st.selectbox("Select UAE ID", uae_ids)

    client_core = df_core[df_core["UAE ID"] == selected_id]
    client_life = df_life[df_life["UAE ID"] == selected_id].iloc[0]
    client_name = client_life["Client Name"]

    st.markdown(f"### 👤 {client_name} ({selected_id})")
    st.markdown(f"- **Nationality**: {client_life['Nationality']}")
    st.markdown(f"- **Property**: {client_life['Property Location']} (AED {client_life['Property Value']:,})")
    st.markdown(f"- **Utility**: AED {client_life['Monthly Utility Bill']} via {client_life['Utility Provider']}")
    st.markdown(f"- **Medical Insurance**: {client_life['Medical Insurance']}")
    st.markdown(f"- **Car**: {client_life['Car Type']} ({client_life['Car Year']})")
    st.markdown(f"- **Credit Card Activity**: {client_life['Credit Card Activity']}")

    # --- Relationship Summary ---
    st.markdown("---")
    st.subheader("🏦 Relationship Summary Across Banks")
    rel_summary = client_core.groupby("Bank")["Products Used"].apply(
        lambda x: ", ".join(sorted(set(x)))
    ).reset_index().rename(columns={"Products Used": "Products Held"})
    st.dataframe(rel_summary.reset_index(drop=True), use_container_width=True)

    # --- AI Recommendations ---
    st.markdown("---")
    st.subheader("🤖 AI Recommendations – Lifestyle-Based")

    ai_recos = []

    if client_life["Medical Insurance"] == "None":
        ai_recos.append({
            "Recommendation": "Offer Medical & Critical Illness Plan",
            "Why": "No current medical insurance.",
            "Logic": "Medical Insurance field = None"
        })

    if client_life["Property Location"] in ["Dubai Marina", "Abu Dhabi Saadiyat"]:
        ai_recos.append({
            "Recommendation": "Recommend Real Estate Investment or REIT",
            "Why": "High-value property location.",
            "Logic": "Luxury location + Property Value > 3M"
        })

    if client_life["Monthly Utility Bill"] > 1000:
        ai_recos.append({
            "Recommendation": "Pitch Energy Efficiency Upgrade Loan",
            "Why": "High utility consumption.",
            "Logic": "Monthly Utility > AED 1000"
        })

    if "Air Tickets" in client_life["Credit Card Activity"]:
        ai_recos.append({
            "Recommendation": "Offer Travel Insurance Add-on",
            "Why": "Frequent air ticket purchases detected.",
            "Logic": "'Air Tickets' in credit card activity"
        })

    if client_life["Nationality"] == "UAE":
        ai_recos.append({
            "Recommendation": "Suggest National Bonds or Waqf Savings Plan",
            "Why": "Available to UAE Nationals only.",
            "Logic": "Nationality = UAE"
        })

    if not ai_recos:
        st.info("✅ No AI recommendations triggered for this profile.")
    else:
        ai_df = pd.DataFrame(ai_recos)
        st.dataframe(ai_df.reset_index(drop=True), use_container_width=True)

    # --- Raw Record Viewer ---
    with st.expander("🧾 View Detailed Product Records"):
        st.dataframe(client_core.reset_index(drop=True), use_container_width=True)
