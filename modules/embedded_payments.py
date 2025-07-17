import streamlit as st

def run_embedded_payments():
    st.header("🔗 Embedded Payments via Agentic AI")

    st.subheader("Use Case A: Voice Refill (e.g., Alexa)")
    if st.button("Simulate Voice Refill"):
        st.write("Agent: 'Detected past 3 recharges of AED 100. Refill wallet with AED 100 now?'")
        st.write("✅ Transfer triggered via PISP. Voice confirmation logged.")

    st.subheader("Use Case B: Embedded Insurance (Car Website)")
    car_model = st.selectbox("Choose EV Model", ["Tesla Model 3", "MG ZS EV", "Nissan Leaf"])
    if st.button("Get Insurance Suggestion"):
        st.write("Agent: 'Based on your age and EV type, here are top 2 insurance options:'")
        st.write("- Noor Takaful: AED 3,400/year
- Orient Insurance: AED 3,750/year (faster claims)")
        st.write("✅ Application pre-filled and payment ready via Aani.")
