
import streamlit as st
import json
import random

# Simulated high-risk corridors and PEP names
HIGH_RISK_COUNTRIES = ["Iran", "Sudan", "North Korea", "Yemen", "Syria"]
SIMULATED_PEP_LIST = ["Ahmed Al Falasi", "Zahra Mansoor", "Javed Qureshi"]

def run_rm_copilot():
    st.header("🧠 RM Copilot and Chatbot")

    with open("data/clients_with_roles.json") as f:
        clients = json.load(f)

    client_names = [client["name"] for client in clients]
    selected_name = st.selectbox("Select a Client", client_names)
    client = next((c for c in clients if c["name"] == selected_name), None)

    st.subheader("📋 Client Profile")
    st.write(f"**Name:** {client['name']}")
    st.write(f"**Income:** AED {client['monthly_income']:,}")
    st.write(f"**Segment:** {client['segment']}")
    st.write(f"**RM Role:** {client['rm_role']}")
    st.write(f"**Products:** {', '.join(client['products'])}")
    st.write(f"**Cars:** {', '.join([f"{car['model']} ({car['fuel']}, {car['year']})" for car in client['cars']])}")

    # --- UAE-Style Risk Engine ---

    st.subheader("🧮 Risk Assessment Breakdown")

    income = client["monthly_income"]
    num_products = len(client["products"])
    fx_country = random.choice(HIGH_RISK_COUNTRIES + ["India", "UK", "Philippines"])  # Simulated
    is_pep = client["name"] in SIMULATED_PEP_LIST
    simulated_credit_score = random.randint(550, 850)

    # Use provided breakdowns if available
    income_score = client.get("risk_breakdown", {}).get("income_score", 3)
    product_score = client.get("risk_breakdown", {}).get("product_mix_score", 3)
    fx_score = 5 if fx_country in HIGH_RISK_COUNTRIES else 2
    pep_score = 10 if is_pep else 0
    credit_score = 1 if simulated_credit_score > 800 else 3 if simulated_credit_score > 650 else 5
    credit_label = "Excellent" if credit_score == 1 else "Moderate" if credit_score == 3 else "High Risk"

    # Final risk score
    total_risk_score = income_score + product_score + fx_score + pep_score + credit_score
    risk_category = (
        "Low" if total_risk_score <= 8 else
        "Moderate" if total_risk_score <= 14 else
        "High"
    )

    st.markdown(f"""
    ✔ **Monthly Income**: AED {income:,} → Risk Score: {income_score}  
    ✔ **Products Held**: {num_products} → Risk Score: {product_score}  
    ✔ **FX Destination**: {fx_country} → Risk Score: {fx_score}  
    ✔ **PEP Check**: {"✅ Flagged" if is_pep else "❌ Not flagged"} → Risk Score: {pep_score}  
    ✔ **Simulated Credit Tier**: {credit_label} (AECB: {simulated_credit_score}) → Risk Score: {credit_score}  

    ### 🧮 Total Risk Score: {total_risk_score} → **Risk Category: {risk_category}**
    """)

    # --- Chatbot Interface ---

    st.divider()
    st.subheader("💬 Ask the RM Copilot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Ask anything about this client...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        def simulate_response(profile, risk_level):
            role = profile.get("rm_role", "General RM")

            role_based_actions = {
                "Private Banker / Wealth RM": ["Offer Wealth Planning Review", "Suggest Premium Takaful", "Invite to Investment Seminar"],
                "Loan Sales RM / Mortgage Specialist": ["Promote Home Loan Balance Transfer", "Offer Property Insurance", "Discuss Repricing Options"],
                "Remittance RM / FX Sales RM": ["Offer FX Wallet", "Promote Low-Fee Corridor Plan", "Suggest Forward Contract"],
                "Credit Card RM / Cards Product Manager": ["Suggest Platinum Card Upgrade", "Offer Cashback Optimization", "Push Summer Travel Offer"],
                "Bancassurance RM / Insurance Advisor": ["Recommend Critical Illness Plan", "Offer Term Life Coverage", "Run Retirement Planning Tool"],
                "Retail RM / Community RM": ["Invite to Financial Fitness Workshop", "Cross-sell Credit Card", "Offer Digital Savings Goal Tracker"]
            }

            actions = role_based_actions.get(role, [
                "Offer Wealth Management Plan",
                "Suggest Takaful Insurance",
                "Promote Visa Infinite Card"
            ])
            selected = random.sample(actions, min(3, len(actions)))
            pitch = f"Hi {profile['name'].split()[0]}, based on your profile, our {selected[0]} could be a great fit this month."
            if risk_level == "High":
                pitch += " (Note: due to high risk profile, further checks may be required.)"
            return f"Suggested Actions:
- {selected[0]}
- {selected[1]}
- {selected[2]}

WhatsApp Pitch:
"{pitch}""

        response = simulate_response(client, risk_category)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])
