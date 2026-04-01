from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from core.rag_engine import answer, load_documents

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / 'data'
DATA.mkdir(parents=True, exist_ok=True)

app = FastAPI(title='production-rag-assistant')
INDEX: list = []


@app.post('/upload')
async def upload(file: UploadFile = File(...)) -> dict:
    target = DATA / file.filename
    with target.open('wb') as f:
        shutil.copyfileobj(file.file, f)
    return {'status': 'uploaded', 'file': file.filename}


@app.post('/reindex')
def reindex() -> dict:
    global INDEX
    INDEX = load_documents(DATA)
    return {'status': 'indexed', 'chunks': len(INDEX)}


@app.post('/ask')
def ask(question: str = Form(...)) -> dict:
    if not INDEX:
        raise HTTPException(status_code=400, detail='Index empty. Upload docs and call /reindex.')
    return answer(question, INDEX)
