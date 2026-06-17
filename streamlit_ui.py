import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.title("🧠AI Assistant for Ticket Support")

# -------------------------
# Ask Question Section
# -------------------------

st.subheader("Ask a Question")

question = st.text_input(
    "Enter your question"
)

if st.button("Ask"):

    try:

        response = requests.post(
            f"{API_URL}/ask",
            json={
                "question": question
            }
        )

        if response.status_code == 200:

            result = response.json()

            st.success("Response Generated")

            st.write(result["answer"])

        else:

            st.error(
                f"Error: {response.status_code}"
            )

    except Exception as e:

        st.error(
            f"Connection Error: {str(e)}"
        )

# -------------------------
# Anomaly Detection Section
# -------------------------

st.title("Anomaly Detection")

if st.button("Show Anomalies"):

    response = requests.get(
        "http://localhost:8000/anomalies"
    ).json()

    anomalies = response["anomalies"]

    st.success(
        f"{len(anomalies)} anomalies detected"
    )

    st.dataframe(
        pd.DataFrame(anomalies)
    )