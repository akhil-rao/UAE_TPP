import streamlit as st
import json
import random

def run_embedded_payments():
    st.header("🚘 Embedded Payments with Vehicle-Aware AI")

    with open("data/clients.json") as f:
        clients = json.load(f)

    client_names = [client["name"] for client in clients]
    selected_name = st.selectbox("Select a Client", client_names)
    client = next((c for c in clients if c["name"] == selected_name), None)

    st.subheader("🧾 Client Assets")
    for car in client["cars"]:
        st.markdown(f"- **{car['model']}** ({car['fuel']}, {car['year']})")

    st.subheader("🛡 Insurance Suggestion")
    selected_car = random.choice(client["cars"])
    st.write(f"Based on your {selected_car['year']} {selected_car['model']} ({selected_car['fuel']}), here are top insurance options:")
    st.write("- Noor Takaful: AED 3,200/year")
    st.write("- Orient Insurance: AED 3,500/year (faster claims)")
    st.success("✅ Application pre-filled and ready for payment via Aani.")
