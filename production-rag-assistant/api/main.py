from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from app.rag_service import ProductionRAGAssistant

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "uploads"
DATA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Production RAG Assistant", version="1.0.0")
assistant: ProductionRAGAssistant | None = None


class AskResponse(BaseModel):
    answer: str
    citations: list[dict]


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)) -> dict:
    path = DATA_DIR / file.filename
    with path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "ok", "file": file.filename}


@app.post("/reindex")
def reindex() -> dict:
    global assistant
    assistant = ProductionRAGAssistant(DATA_DIR)
    return {"status": "ok", "chunks": len(assistant.chunks)}


@app.post("/ask", response_model=AskResponse)
def ask(question: str = Form(...)) -> AskResponse:
    if assistant is None:
        raise HTTPException(status_code=400, detail="Index is empty. Upload docs and call /reindex first.")
    result = assistant.ask(question)
    citations = [c.__dict__ for c in result.citations]
    return AskResponse(answer=result.answer, citations=citations)
