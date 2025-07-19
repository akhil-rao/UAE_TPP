import streamlit as st
import json
import random

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
    st.write(f"**Segment:** {client['segment']}")
    st.write(f"**RM Role:** {client.get('rm_role', 'General RM')}")
    st.write(f"**Products:** {', '.join(client['products'])}")
    st.write("**Cars:**")
    for car in client["cars"]:
        st.markdown(f"- {car['model']} ({car['fuel']}, {car['year']})")

    # --- Risk Engine ---

    st.subheader("🧮 Risk Assessment Breakdown")

    income_score = client.get("risk_breakdown", {}).get("income_score", 3)
    product_score = client.get("risk_breakdown", {}).get("product_mix_score", 3)
    fx_country = random.choice(HIGH_RISK_COUNTRIES + ["India", "UK", "Philippines"])
    fx_score = 5 if fx_country in HIGH_RISK_COUNTRIES else 2
    is_pep = client["name"] in SIMULATED_PEP_LIST
    pep_score = 10 if is_pep else 0
    credit_sim = random.randint(550, 850)
    credit_score = 1 if credit_sim > 800 else 3 if credit_sim > 650 else 5
    credit_label = "Excellent" if credit_score == 1 else "Moderate" if credit_score == 3 else "High Risk"

    total_score = income_score + product_score + fx_score + pep_score + credit_score
    if total_score <= 8:
        risk_cat = "Low"
    elif total_score <= 14:
        risk_cat = "Moderate"
    else:
        risk_cat = "High"

    st.markdown(f"""
    ✔ **Monthly Income** → Score: {income_score}  
    ✔ **Products Held** → Score: {product_score}  
    ✔ **FX Destination**: {fx_country} → Score: {fx_score}  
    ✔ **PEP Check**: {"✅ Flagged" if is_pep else "❌ Not flagged"} → Score: {pep_score}  
    ✔ **Simulated Credit Score**: {credit_sim} → {credit_label} → Score: {credit_score}  

    ### 🧮 Total Risk Score: {total_score} → **{risk_cat} Risk**
    """)

    # --- Copilot Chatbot ---

    st.divider()
    st.subheader("💬 Ask the RM Copilot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Ask anything about this client...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        def simulate_response(client, risk):
            role = client.get("rm_role", "General RM")

            suggestions = {
                "Private Banker / Wealth RM": [
                    "Offer Wealth Planning Review",
                    "Suggest Premium Takaful",
                    "Invite to Investment Seminar"
                ],
                "Loan Sales RM / Mortgage Specialist": [
                    "Promote Home Loan Balance Transfer",
                    "Offer Property Insurance",
                    "Discuss Repricing Options"
                ],
                "Remittance RM / FX Sales RM": [
                    "Offer FX Wallet",
                    "Promote Low-Fee Corridor Plan",
                    "Suggest Forward Contract"
                ],
                "Credit Card RM / Cards Product Manager": [
                    "Suggest Platinum Card Upgrade",
                    "Offer Cashback Optimization",
                    "Push Summer Travel Offer"
                ],
                "Bancassurance RM / Insurance Advisor": [
                    "Recommend Critical Illness Plan",
                    "Offer Term Life Coverage",
                    "Run Retirement Planning Tool"
                ],
                "Retail RM / Community RM": [
                    "Invite to Financial Fitness Workshop",
                    "Cross-sell Credit Card",
                    "Offer Digital Savings Goal Tracker"
                ]
            }

            actions = suggestions.get(role, [
                "Offer Wealth Management Plan",
                "Suggest Takaful Insurance",
                "Promote Visa Infinite Card"
            ])
            pick = random.sample(actions, 3)
            pitch = f"Hi {client['name'].split()[0]}, our {pick[0]} could be ideal this month."
            if risk == "High":
                pitch += " (Further checks may apply due to high risk.)"
            return f"Suggested Actions:\n- {pick[0]}\n- {pick[1]}\n- {pick[2]}\n\nPitch:\n\"{pitch}\""

        result = simulate_response(client, risk_cat)
        st.session_state.chat_history.append({"role": "assistant", "content": result})

    for msg in st.session_state.chat_history:
        speaker = "user" if msg["role"] == "user" else "assistant"
        st.chat_message(speaker).write(msg["content"])
