import streamlit as st
import json
import random

def run_rm_copilot():
    st.header("🧠 RM Copilot Chatbot (Simulated)")

    # Load clients
    with open("data/clients.json") as f:
        clients = json.load(f)

    client_names = [client["name"] for client in clients]
    selected_name = st.selectbox("Select a Client", client_names)

    selected_client = next((c for c in clients if c["name"] == selected_name), None)

    st.subheader("Client Profile")
    st.write(f"**Income:** AED {selected_client['monthly_income']:,}")
    st.write(f"**Segment:** {selected_client['segment']}")
    st.write(f"**Products:** {', '.join(selected_client['products'])}")
    st.write(f"**Risk Score:** {selected_client['risk_score']}")

    st.divider()
    st.subheader("💬 Chat with RM Copilot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Ask anything about this client...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Simulated GPT-style logic
        def simulate_response(profile, query):
            actions = random.sample([
                "Recommend Life Insurance",
                "Offer Elite Travel Credit Card",
                "Suggest Investment Plan",
                "Cross-sell Home Insurance",
                "Propose Salary Advance",
                "Invite to Wealth Seminar"
            ], 3)
            pitch = f"Hi {profile['name'].split()[0]}, based on your profile, I’d recommend our new {actions[0]} offering this month."

            return f"Suggested Actions:
- {actions[0]}
- {actions[1]}
- {actions[2]}

WhatsApp Pitch:
"{pitch}""

        reply = simulate_response(selected_client, user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])
