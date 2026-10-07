import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline import get_answer

app = FastAPI()

class AskRequest(BaseModel):
    question: str
    language: str = "English"

@app.post("/ask")
def ask(req: AskRequest):
    answer, matched = get_answer(req.question, req.language)
    return {"answer": answer, "matched_question": matched}