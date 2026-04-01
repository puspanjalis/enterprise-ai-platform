from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(slots=True)
class Chunk:
    id: str
    source: str
    text: str


def load_documents(data_dir: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(data_dir.glob('*')):
        if path.suffix.lower() not in {'.md', '.txt'} or not path.is_file():
            continue
        text = path.read_text(encoding='utf-8')
        cleaned = ' '.join(text.split())
        for idx, start in enumerate(range(0, len(cleaned), 500)):
            part = cleaned[start:start+650].strip()
            if part:
                chunks.append(Chunk(id=f'{path.name}:{idx}', source=path.name, text=part))
    return chunks


def _tokenize(text: str) -> set[str]:
    return {t.strip('.,!?():;').lower() for t in text.split() if t.strip()}


def retrieve(question: str, chunks: Iterable[Chunk], top_k: int = 4) -> list[Chunk]:
    q = _tokenize(question)
    scored = []
    for chunk in chunks:
        overlap = len(q.intersection(_tokenize(chunk.text)))
        scored.append((overlap, chunk))
    scored.sort(key=lambda row: row[0], reverse=True)
    return [chunk for score, chunk in scored[:top_k] if score > 0]


def answer(question: str, chunks: list[Chunk]) -> dict:
    matches = retrieve(question, chunks)
    if not matches:
        return {
            'answer': "I couldn't find grounded evidence in the indexed documents.",
            'citations': [],
        }
    bullets = '\n'.join([f"- {m.text[:220]}..." for m in matches])
    return {
        'answer': f"Grounded answer for: {question}\n\nEvidence:\n{bullets}",
        'citations': [{'id': m.id, 'source': m.source, 'snippet': m.text[:260]} for m in matches],
    }
