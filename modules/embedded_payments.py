import streamlit as st
import json
import random

def run_embedded_payments():
    st.header("🚘 Embedded Payments with Vehicle-Aware AI")

    # Load clients
    with open("data/clients.json") as f:
        clients = json.load(f)

    client_names = [client["name"] for client in clients]
    selected_name = st.selectbox("Select a Client", client_names)
    client = next((c for c in clients if c["name"] == selected_name), None)

    st.subheader("🧾 Client Assets")
    for car in client["cars"]:
        st.markdown(f"- **{car['model']}** ({car['fuel']}, {car['year']})")

    selected_car = random.choice(client["cars"])
    car_desc = f"{selected_car['year']} {selected_car['model']} ({selected_car['fuel']})"

    # ---- Segment Classification ----
    income = client["monthly_income"]
    num_products = len(client["products"])
    premium_car_models = ["Ferrari", "BMW 7 Series", "Range Rover", "Land Cruiser"]
    owns_premium = any(car["model"] in premium_car_models for car in client["cars"])

    if income > 40000 and num_products >= 3 and owns_premium:
        segment = "High Net Worth"
    elif income > 10000 and num_products >= 2:
        segment = "Affluent"
    else:
        segment = "Mass"

    # ---- AI-Powered Recommendation ----
    if segment == "High Net Worth":
        recommended = "Orient Insurance"
        reason = (
            "You are classified as a High Net Worth client based on income, "
            "product holdings, and vehicle ownership. Orient offers premium service quality."
        )
    elif segment == "Affluent":
        recommended = "Orient Insurance"
        reason = (
            "As an Affluent segment client, you would benefit from balanced coverage "
            "and faster claims via Orient."
        )
    else:
        recommended = "Noor Takaful"
        reason = (
            "As a cost-conscious Mass segment client, Noor Takaful offers better value "
            "for essential coverage."
        )

    # ---- UI Output ----
    st.subheader("🤖 AI Recommendation")
    st.info(f"**Recommended:** {recommended}\n\n🧠 {reason}")

    st.subheader("🛡 Insurance Options")
    st.markdown(f"### Based on the clients **{car_desc}**, here are your top insurance options:")

    st.markdown("#### 1️⃣ Noor Takaful")
    st.markdown(
        "- ✅ Lower premium (**AED 3,200/year**)\n"
        "- 🔄 Claim turnaround: ~7 days\n"
        "- 🔒 Includes off-road cover\n"
        "- ⚠️ No roadside pickup\n"
        "**Best for:** Cost-conscious users with standard coverage needs"
    )

    st.markdown("---")

    st.markdown("#### 2️⃣ Orient Insurance")
    st.markdown(
        "- 💼 Premium: **AED 3,500/year**\n"
        "- ⚡ Fast-track claims: ~3 days\n"
        "- 🛠 500+ agency repair centers\n"
        "- 🚗 Includes courtesy car + pickup/drop\n"
        "**Best for:** Premium clients who value speed and convenience"
    )

    st.success("✅ Application is pre-filled and ready for payment via Aani.")
