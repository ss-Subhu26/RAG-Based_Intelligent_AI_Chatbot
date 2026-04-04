import streamlit as st
import requests

st.title("RAG AI Chatbot")

uploaded_file = st.file_uploader("Upload PDF")

if uploaded_file:
    files = {"file": uploaded_file}
    requests.post("http://localhost:8000/upload", files=files)
    st.success("File uploaded!")

query = st.text_input("Ask a question")

if st.button("Ask"):
    res = requests.post(
        "http://localhost:8000/ask",
        params={"query": query}
    )
    st.write(res.json())