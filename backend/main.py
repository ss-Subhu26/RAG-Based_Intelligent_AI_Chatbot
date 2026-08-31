from fastapi import FastAPI, UploadFile, File, HTTPException

from backend.ragpipeline import add_documents, get_answer

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import shutil
import os
import uuid

app = FastAPI(
    title="RAG PDF Chatbot API"
)

# --------------------------------------------------

# Home

# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "RAG PDF Chatbot API is running"
    }


# --------------------------------------------------

# Upload PDF

# --------------------------------------------------

@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    # Check file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Create temporary filename
    file_id = str(uuid.uuid4())
    file_path = f"temp_{file_id}.pdf"

    try:

        # Save uploaded PDF
        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # Load PDF
        loader = PyPDFLoader(file_path)

        pages = loader.load()

        if not pages:

            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF."
            )

        # --------------------------------------------------
        # Split text into chunks
        # --------------------------------------------------

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        documents = splitter.split_documents(pages)

        # --------------------------------------------------
        # Add embeddings to ChromaDB
        # --------------------------------------------------

        count = add_documents(documents)

        return {
            "message": "PDF uploaded and processed successfully.",
            "filename": file.filename,
            "pages": len(pages),
            "chunks": count
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        # Delete temporary PDF
        if os.path.exists(file_path):

            os.remove(file_path)


# --------------------------------------------------

# Ask Question

# --------------------------------------------------

@app.post("/ask")
def ask_question(query: str):
    if not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        answer = get_answer(query)

        return {
            "query": query,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

