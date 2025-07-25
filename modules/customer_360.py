import streamlit as st
import pandas as pd

def run():
    st.set_page_config(page_title="Customer 360 View", layout="wide")
    st.title("📊 Customer 360 View – Unified Profile with AI Insights")

    # Load bank + lifestyle data
    @st.cache_data
    def load_data():
        df_core = pd.read_csv("data/client_profile_summary.csv")
        df_life = pd.DataFrame([
            {
                "UAE ID": "784-1234-567890-1", "Client Name": "Fatima Al Mansouri", "Nationality": "UAE",
                "Property Location": "Dubai Marina", "Property Value": 3100000, "Utility Provider": "DEWA",
                "Monthly Utility Bill": 1450, "Medical Insurance": "None", "Credit Card Activity": "Air Tickets, Groceries",
                "Car Info Source": "RSA Insurance", "Car Type": "BMW 7 Series", "Car Year": 2023
            },
            {
                "UAE ID": "784-9876-543210-2", "Client Name": "Omar Al Fardan", "Nationality": "Expat",
                "Property Location": "Sharjah Al Khan", "Property Value": 1200000, "Utility Provider": "SEWA",
                "Monthly Utility Bill": 650, "Medical Insurance": "Yes (AXA)", "Credit Card Activity": "Online Shopping",
                "Car Info Source": "Oman Insurance", "Car Type": "Toyota Prado", "Car Year": 2021
            },
            {
                "UAE ID": "784-2468-135790-3", "Client Name": "Salim Khan", "Nationality": "Expat",
                "Property Location": "Business Bay", "Property Value": 2150000, "Utility Provider": "DEWA",
                "Monthly Utility Bill": 980, "Medical Insurance": "None", "Credit Card Activity": "Air Tickets, Dining",
                "Car Info Source": "Orient Insurance", "Car Type": "Tesla Model Y", "Car Year": 2024
            },
            {
                "UAE ID": "784-3698-147025-4", "Client Name": "Laila Hassan", "Nationality": "UAE",
                "Property Location": "Abu Dhabi Saadiyat", "Property Value": 5800000, "Utility Provider": "ADDC",
                "Monthly Utility Bill": 1950, "Medical Insurance": "Yes (Daman)", "Credit Card Activity": "Luxury Retail, Travel",
                "Car Info Source": "Tokio Marine", "Car Type": "Range Rover", "Car Year": 2022
            }
        ])
        return df_core, df_life

    df_core, df_life = load_data()

    # --- Filter by UAE ID ---
    uae_ids = sorted(df_life["UAE ID"].unique())
    selected_id = st.selectbox("Select Client (by UAE ID)", uae_ids)

    client_core = df_core[df_core["UAE ID"] == selected_id]
    client_life = df_life[df_life["UAE ID"] == selected_id].iloc[0]
    client_name = client_life["Client Name"]

    st.markdown(f"### 👤 {client_name} ({selected_id})")
    st.markdown(f"- **Nationality**: {client_life['Nationality']}")
    st.markdown(f"- **Property**: {client_life['Property Location']} (AED {client_life['Property Value']:,})")
    st.markdown(f"- **Medical Insurance**: {client_life['Medical Insurance']}")
    st.markdown(f"- **Utility Bill**: AED {client_life['Monthly Utility Bill']} via {client_life['Utility Provider']}")
    st.markdown(f"- **Car**: {client_life['Car Type']} ({client_life['Car Year']}) via {client_life['Car Info Source']}")
    st.markdown(f"- **Card Usage**: {client_life['Credit Card Activity']}")

    st.markdown("---")
    st.subheader("🏦 Relationship Summary Across Banks")
    rel_summary = client_core.groupby("Bank")["Products Used"].apply(
        lambda x: ", ".join(sorted(x.unique()))
    ).reset_index().rename(columns={"Products Used": "Products Held"})
    st.dataframe(rel_summary, use_container_width=True)

    st.markdown("---")
    st.subheader("🤖 AI Recommendations – Tailored to Lifestyle")

    ai_recos = []

    if client_life["Medical Insurance"] == "None":
        ai_recos.append({
            "Recommendation": "Offer Medical & Critical Illness Plan",
            "Why": "No current insurance detected.",
            "Logic": "client['Medical Insurance'] == 'None'"
        })

    if client_life["Property Location"] in ["Dubai Marina", "Abu Dhabi Saadiyat"]:
        ai_recos.append({
            "Recommendation": "Recommend Real Estate Income Plan or REIT",
            "Why": "High-value property location.",
            "Logic": "Property in premium zone + Value > AED 3M"
        })

    if client_life["Monthly Utility Bill"] > 1000:
        ai_recos.append({
            "Recommendation": "Offer Energy Efficiency Upgrade Loan",
            "Why": "High monthly utilities indicate large property or inefficient systems.",
            "Logic": "Monthly Utility > 1000 AED"
        })

    if "Air Tickets" in client_life["Credit Card Activity"]:
        ai_recos.append({
            "Recommendation": "Bundle Travel Insurance",
            "Why": "Frequent air ticket spend detected.",
            "Logic": "'Air Tickets' in credit card purchases"
        })

    if client_life["Nationality"] == "UAE":
        ai_recos.append({
            "Recommendation": "Suggest National Bonds or Waqf Savings Plan",
            "Why": "Available to UAE Nationals.",
            "Logic": "client['Nationality'] == 'UAE'"
        })

    if not ai_recos:
        st.info("✅ No AI recommendations at this time.")
    else:
        ai_df = pd.DataFrame(ai_recos)
        st.dataframe(ai_df, use_container_width=True)

    # Optional raw view
    with st.expander("🧾 View All Bank Records for This Client"):
        st.dataframe(client_core, use_container_width=True)
