import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def run_rm_copilot():
    st.header("🧠 RM / Advisor Copilot")

    st.subheader("Client Radar View")
    radar_df = pd.read_csv("data/client_radar.csv")
    categories = radar_df["category"]
    values = radar_df["value"].tolist()
    values += values[:1]

    angles = [n / float(len(categories)) * 2 * np.pi for n in range(len(categories))]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.3)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    st.pyplot(fig)

    st.subheader("Pitch Coach")
    if st.button("Generate Pitch"):
        st.success("Hi Fatima, based on your travel pattern, our new Elite Travel Card could save you AED 700/year.")
