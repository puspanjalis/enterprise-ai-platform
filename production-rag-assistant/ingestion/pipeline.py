from __future__ import annotations

from pathlib import Path

from ingestion.chunker import chunk_text
from ingestion.loaders import load_document
from ingestion.types import DocumentChunk


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".md", ".markdown", ".txt", ".rst"}


def ingest_directory(path: Path) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []
    for file in sorted(path.rglob("*")):
        if not file.is_file() or file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        for text, page in load_document(file):
            chunks.extend(chunk_text(text=text, source=file.name, page=page))
    return chunks
