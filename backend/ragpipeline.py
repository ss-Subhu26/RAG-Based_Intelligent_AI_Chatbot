import os

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# --------------------------------------------------

# Configuration

# --------------------------------------------------

CHROMA_DIR = "./chroma_db"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
 raise ValueError(
"GROQ_API_KEY is not set. Add it to your .env file."
)

# --------------------------------------------------

# Embedding Model

# --------------------------------------------------

embeddings = HuggingFaceEmbeddings(
model_name="BAAI/bge-base-en-v1.5"
)

# --------------------------------------------------

# ChromaDB

# --------------------------------------------------

vectorstore = Chroma(
collection_name="pdf_documents",
persist_directory=CHROMA_DIR,
embedding_function=embeddings
)

# --------------------------------------------------

# LLM

# --------------------------------------------------
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=GROQ_API_KEY
)

# --------------------------------------------------

# Prompt

# --------------------------------------------------

prompt = ChatPromptTemplate.from_template(
"""
You are a helpful AI assistant.

Answer the question using ONLY the context provided below.

If the answer is not available in the context, say:

"I could not find the answer in the uploaded PDF."

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""
)

# --------------------------------------------------

# Add PDF documents to ChromaDB

# --------------------------------------------------

def add_documents(documents):


 if not documents:
    return 0

 vectorstore.add_documents(documents)

 return len(documents)


# --------------------------------------------------

# Question Answering

# --------------------------------------------------

def get_answer(query: str):

    if not query or not query.strip():
        return "Please enter a question."

    # Retrieve relevant chunks
    documents = vectorstore.similarity_search(
        query,
        k=4
    )

    if not documents:
        return "No relevant information was found in the uploaded PDF."

    # Combine retrieved chunks
    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    # Create prompt
    messages = prompt.invoke(
        {
            "context": context,
            "question": query
        }
    )

    # Generate answer
    response = llm.invoke(messages)

    return response.content

