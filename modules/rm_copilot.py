import streamlit as st
import json
import random

# Simulated high-risk corridors and PEP names (for demo)
HIGH_RISK_COUNTRIES = ["Iran", "Sudan", "North Korea", "Yemen", "Syria"]
SIMULATED_PEP_LIST = ["Ahmed Al Falasi", "Zahra Mansoor", "Javed Qureshi"]

def run_rm_copilot():
    st.header("🧠 RM Copilot and Chatbot")

    with open("data/clients.json") as f:
        clients = json.load(f)

    client_names = [client["name"] for client in clients]
    selected_name = st.selectbox("Select a Client", client_names)
    client = next((c for c in clients if c["name"] == selected_name), None)

    st.subheader("📋 Client Profile")
    st.write(f"**Name:** {client['name']}")
    st.write(f"**Income:** AED {client['monthly_income']:,}")
    st.write(f"**Products:** {', '.join(client['products'])}")
    st.write(f"**Cars:** {', '.join([car['model'] for car in client['cars']])}")

    # --- UAE-Style Risk Engine ---

    st.subheader("🧮 Risk Assessment Breakdown")

    income = client["monthly_income"]
    num_products = len(client["products"])
    fx_country = random.choice(HIGH_RISK_COUNTRIES + ["India", "UK", "Philippines"])  # Simulated
    is_pep = client["name"] in SIMULATED_PEP_LIST
    simulated_credit_score = random.randint(550, 850)

    # 1. Income-based risk score
    if income > 50000:
        income_score = 1
    elif income > 20000:
        income_score = 2
    elif income > 10000:
        income_score = 3
    else:
        income_score = 4

    # 2. Product diversity risk
    if num_products >= 4:
        product_score = 1
    elif num_products == 3:
        product_score = 2
    elif num_products == 2:
        product_score = 3
    else:
        product_score = 4

    # 3. FX corridor risk
    fx_score = 5 if fx_country in HIGH_RISK_COUNTRIES else 2

    # 4. PEP / sanctions risk
    pep_score = 10 if is_pep else 0

    # 5. Credit score proxy
    if simulated_credit_score > 800:
        credit_score = 1
        credit_label = "Excellent"
    elif simulated_credit_score > 650:
        credit_score = 3
        credit_label = "Moderate"
    else:
        credit_score = 5
        credit_label = "High Risk"

    # Final risk score
    total_risk_score = income_score + product_score + fx_score + pep_score + credit_score

    if total_risk_score <= 8:
        risk_category = "Low"
    elif total_risk_score <= 14:
        risk_category = "Moderate"
    else:
        risk_category = "High"

    # Display risk breakdown
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
            actions = random.sample([
                "Offer Wealth Management Plan",
                "Suggest Takaful Insurance",
                "Recommend FX Subscription Pack",
                "Flag for Enhanced Due Diligence",
                "Promote Visa Infinite Card"
            ], 3)

            pitch = f"Hi {profile['name'].split()[0]}, based on your profile, our {actions[0]} could be a great fit this month."
            if risk_level == "High":
                pitch += " (Note: due to high risk profile, further checks may be required.)"
            return f"Suggested Actions:\n- {actions[0]}\n- {actions[1]}\n- {actions[2]}\n\nWhatsApp Pitch:\n\"{pitch}\""

        response = simulate_response(client, risk_category)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])
