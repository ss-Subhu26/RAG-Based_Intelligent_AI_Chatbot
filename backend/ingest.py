from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
def ingest_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    vectorstore = Chroma.from_documents(
        chunks,
        embedding=None,  # replace with OpenAI embeddings later
        persist_directory="./db"
    )

    vectorstore.persist()
    return "Data stored successfully!"