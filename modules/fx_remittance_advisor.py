import streamlit as st

def run_fx_advisor():
    st.header("💱 FX Remittance Advisor")

    amount = st.number_input("Amount to Send (AED)", min_value=0.0)
    destination = st.selectbox("Destination Country", ["India", "UK", "Philippines", "Pakistan", "UAE"])
    urgency = st.selectbox("Urgency", ["Standard", "Same-day", "Instant"])

    if st.button("Get FX Recommendation"):
        st.subheader("🔍 FX Suggestion")
        if urgency == "Instant":
            st.write("Use: InstaRemit Pro (delivery within seconds)")
        else:
            st.write("Use: SmartFX Saver (best rate, 0.5% margin)")
