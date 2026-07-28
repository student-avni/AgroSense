import streamlit as st
from rag_pipeline import get_answer

st.set_page_config(page_title="AgroSense - AI Farming Assistant", page_icon="🌾")

st.title("🌾 AgroSense - AI Farming Assistant")
st.write("Ask any farming question and get instant AI-powered advice.")

user_query = st.text_input("Enter your farming question:")

if st.button("Get Answer"):
    if user_query:
        with st.spinner("Thinking..."):
            answer = get_answer(user_query)
        st.success(answer)
    else:
        st.warning("Please enter a question first.")