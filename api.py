import sqlite3
from datetime import datetime
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
def init_db():
    conn = sqlite3.connect("agrosense.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        language TEXT,
        created_at TEXT)""")
    conn.commit()
    conn.close()

init_db()
def ask(req: AskRequest):
    answer, matched = get_answer(req.question, req.language)
    return {"answer": answer, "matched_question": matched}