Project Name- RAG-Based_Intelligent AI_Chatbot

# RAG-Based Intelligent AI Chatbot

A domain-specific Retrieval-Augmented Generation (RAG) chatbot that grounds responses in a vector-embedded knowledge base to minimize hallucinations, built to handle production-scale query volume.

## Problem

General-purpose LLMs hallucinate on domain-specific questions. This chatbot retrieves relevant context from a curated knowledge base before generating a response, so answers stay grounded in real source material.

## How It Works

- Source documents are split using semantic chunking (not naive fixed-size splitting) to preserve meaning per chunk.
- Chunks are embedded and stored in ChromaDB.
- On each query, the top-k relevant chunks are retrieved and injected into a grounded prompt template before being sent to the LLM via LangChain.
- FastAPI serves the chatbot as an API; Streamlit provides a simple chat UI.

## Tech Stack

- RAG Framework: LangChain
- Vector Store: ChromaDB
- Backend: FastAPI
- UI:Streamlit

## Results

- Retrieval/response accuracy improved from 65% → 91%
- Supports 1,000+ daily production queries

## Setup

```bash
git clone <repo-url>
cd RAG-Based_Intelligent AI_Chatbot
pip install -r requirements.txt
cp .env.example .env   # add LLM API key
ingest.py       # chunking
rag.py  # embed source docs into ChromaDB
streamlit run app.py
```

## Usage

1. Launch the Streamlit app and ask domain questions in the chat UI.
2. Responses are grounded in retrieved chunks, shown alongside source citations.

## Project Structure

```
├── app.py              # Streamlit chat UI
├── ingest.py            # Chunking + # LangChain retrieval 
├── rag.py           #prompt logic
├── requirements.txt
└── .env.example
```

## Notes

Built as part of a Generative AI Developer internship at Infotact Solutions.

