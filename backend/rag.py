from langchain_community.vectorstores import Chroma

def get_answer(query):
    vectorstore = Chroma(persist_directory="./db", embedding_function=None)

    docs = vectorstore.similarity_search(query, k=3)

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
    Answer ONLY from this context:
    {context}

    Question: {query}
    """

    return {"answer": prompt, "sources": docs}