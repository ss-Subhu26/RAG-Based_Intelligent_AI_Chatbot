from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def home():
    return { "message": "Server running"}

@app.post("/ask")
def ask_question(query:str):
    answer = "get_answer"(query)
    return { "answer": answer}
