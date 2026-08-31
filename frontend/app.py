import streamlit as st
import requests

# --------------------------------------------------

# Page configuration

# --------------------------------------------------

st.set_page_config(
page_title="RAG PDF Chatbot",
page_icon="📚"
)

st.title("📚 RAG-Based Intelligent AI Chatbot")

st.write(
"Upload a PDF and ask questions about its content."
)

# --------------------------------------------------

# PDF Upload

# --------------------------------------------------

st.subheader("1. Upload PDF")

uploaded_file = st.file_uploader(
"Choose a PDF file",
type=["pdf"]
)

if uploaded_file is not None:

    if st.button("Upload & Process PDF"):

     with st.spinner(
        "Reading PDF and creating embeddings..."
    ):

        try:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            response = requests.post(
                "http://127.0.0.1:8000/upload",
                files=files
            )

            if response.status_code == 200:

                result = response.json()

                st.success(
                    result["message"]
                )

                st.info(
                    f"Pages: {result['pages']} | "
                    f"Chunks: {result['chunks']}"
                )

            else:

                st.error(
                    f"Upload failed: {response.text}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI. "
                "Please start the backend server."
            )


# --------------------------------------------------

# Question

# --------------------------------------------------

st.subheader("2. Ask a Question")

query = st.text_input(
"Enter your question:"
)

if st.button("Ask"):


 if not query.strip():

    st.warning(
        "Please enter a question."
    )

else:

    with st.spinner(
        "Searching the PDF and generating answer..."
    ):

        try:

            response = requests.post(
                "http://127.0.0.1:8000/ask",
                params={
                    "query": query
                }
            )

            if response.status_code == 200:

                result = response.json()

                st.subheader("Answer")

                st.write(
                    result["answer"]
                )

            else:

                st.error(
                    f"Error: {response.text}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI. "
                "Please start the backend server."
            )

