import streamlit as st
import requests

st.set_page_config(page_title="AgroSense - AI Farming Assistant", page_icon="🌾")

st.title("🌾 AgroSense - AI Farming Assistant")
st.write("Ask any farming question and get instant AI-powered advice.")

# Point 3: Language toggle
language = st.selectbox("Choose language / भाषा चुनें", ["English", "Hindi"])

user_query = st.text_input("Enter your farming question:")

if st.button("Get Answer"):
    if user_query:
        with st.spinner("Thinking..."):
            res = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"question": user_query, "language": language},
                timeout=60,
            )
            data = res.json()
            answer = data["answer"]
            matched_question = data["matched_question"]
        st.success(answer)

        # Point 2: Show matched source (only if something was actually retrieved)
        if matched_question:
            with st.expander("See matched knowledge base entry"):
                st.write(f"**Matched Question:** {matched_question}")
    else:
        st.warning("Please enter a question first.")