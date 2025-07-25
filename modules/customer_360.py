import streamlit as st
import pandas as pd

def run():
    st.set_page_config(page_title="Customer 360 View", layout="wide")
    st.title("📊 Customer 360 View – With Risk Profiling & AI")

    @st.cache_data
    def load_data():
        lifestyle = pd.DataFrame([
            {"UAE ID": "784-1234-567890-1", "Client Name": "Fatima Al Mansouri", "Nationality": "UAE",
             "Property Location": "Dubai Marina", "Property Value": 3100000, "Utility Bill": 1450,
             "Medical Insurance": "None", "Credit Card Activity": "Air Tickets"},
            {"UAE ID": "784-9876-543210-2", "Client Name": "Omar Al Fardan", "Nationality": "Expat",
             "Property Location": "Sharjah Al Khan", "Property Value": 1200000, "Utility Bill": 650,
             "Medical Insurance": "Yes", "Credit Card Activity": "Online Shopping"},
            {"UAE ID": "784-2468-135790-3", "Client Name": "Salim Khan", "Nationality": "Expat",
             "Property Location": "Business Bay", "Property Value": 2150000, "Utility Bill": 980,
             "Medical Insurance": "None", "Credit Card Activity": "Dining"},
            {"UAE ID": "784-3698-147025-4", "Client Name": "Laila Hassan", "Nationality": "UAE",
             "Property Location": "Abu Dhabi Saadiyat", "Property Value": 5800000, "Utility Bill": 1950,
             "Medical Insurance": "Yes", "Credit Card Activity": "Travel"}
        ])
        usage = pd.read_csv("data/multi_bank_profile.csv")
        return usage, lifestyle

    df_core, df_life = load_data()

    # --- Client Selector
    uae_ids = sorted(df_life["UAE ID"].unique())
    selected_id = st.selectbox("Select UAE ID", uae_ids)

    client_core = df_core[df_core["UAE ID"] == selected_id]
    client_life = df_life[df_life["UAE ID"] == selected_id].iloc[0]
    client_name = client_life["Client Name"]

    # --- Risk Score Logic
    bank_count = client_core["Bank"].nunique()
    score = 0
    reasons = []

    if client_life["Nationality"] == "Expat":
        score += 2
        reasons.append("Expat profile (+2)")

    if client_life["Utility Bill"] > 1000:
        score += 2
        reasons.append("High utility bill (>AED 1000) (+2)")

    if client_life["Medical Insurance"] == "None":
        score += 2
        reasons.append("No medical insurance (+2)")

    if client_life["Property Value"] > 3000000:
        score += 1
        reasons.append("High property value (>AED 3M) (+1)")

    if bank_count >= 4:
        score += 1
        reasons.append("Fragmented holdings across 4 banks (+1)")

    if score <= 2:
        level = "🟢 Low"
    elif score <= 4:
        level = "🟡 Moderate"
    else:
        level = "🔴 High"

    # --- UI Output
    st.markdown(f"### 👤 {client_name} ({selected_id})")
    st.markdown(f"- **Nationality**: {client_life['Nationality']}")
    st.markdown(f"- **Property**: {client_life['Property Location']} (AED {client_life['Property Value']:,})")
    st.markdown(f"- **Utility Bill**: AED {client_life['Utility Bill']}")
    st.markdown(f"- **Medical Insurance**: {client_life['Medical Insurance']}")
    st.markdown(f"- **Credit Activity**: {client_life['Credit Card Activity']}")

    st.markdown("---")
    st.subheader("🛡 Client Risk Profile")
    st.markdown(f"**Risk Level:** {level}  \n**Score:** {score} / 8")
    with st.expander("🧠 How This Risk Was Calculated"):
        for r in reasons:
            st.markdown(f"- {r}")

    # --- Relationship Summary
    st.markdown("---")
    st.subheader("🏦 Relationship Summary Across Banks")
    rel_summary = client_core.groupby("Bank")["Products Used"].apply(
        lambda x: ", ".join(sorted(set(x)))
    ).reset_index().rename(columns={"Products Used": "Products Held"})
    st.dataframe(rel_summary.reset_index(drop=True), use_container_width=True)

    # --- AI Recommendations
    st.markdown("---")
    st.subheader("🤖 AI Recommendations")

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
            "Logic": "Property > AED 3M in prime area"
        })

    if client_life["Utility Bill"] > 1000:
        ai_recos.append({
            "Recommendation": "Offer Green Energy Efficiency Loan",
            "Why": "High electricity/water usage.",
            "Logic": "Utility Bill > AED 1000"
        })

    if "Air Tickets" in client_life["Credit Card Activity"]:
        ai_recos.append({
            "Recommendation": "Recommend Travel Insurance Add-on",
            "Why": "Frequent air ticket purchases detected.",
            "Logic": "'Air Tickets' in Credit Card Activity"
        })

    if client_life["Nationality"] == "UAE":
        ai_recos.append({
            "Recommendation": "Suggest National Bonds or Waqf Savings",
            "Why": "Available only to UAE Nationals.",
            "Logic": "Nationality = UAE"
        })

    if ai_recos:
        ai_df = pd.DataFrame(ai_recos)
        st.dataframe(ai_df.reset_index(drop=True), use_container_width=True)
    else:
        st.success("✅ No AI alerts triggered for this profile.")

    # --- Raw Viewer
    with st.expander("🧾 View Detailed Product Records"):
        st.dataframe(client_core.reset_index(drop=True), use_container_width=True)
