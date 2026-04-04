from fastapi import FastAPI, UploadFile, File
from rag import get_answer
from ingest import ingest_pdf
import shutil 

app = FastAPI()
@app.get("/")
def home():
    return { "message": "Server running"}
@app.post("/upload")
def upload_file(file: UploadFile= File(...)):
    file_path =f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
        ingest_pdf(file_path)
        return {"message": "File processed successfully"}


@app.post("/ask")
def ask_question(query:str):
    return get_answer(query)
