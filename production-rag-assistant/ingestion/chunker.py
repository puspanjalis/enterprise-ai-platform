from __future__ import annotations

from ingestion.types import DocumentChunk


def chunk_text(
    text: str,
    source: str,
    page: int | None,
    chunk_size: int = 700,
    overlap: int = 120,
) -> list[DocumentChunk]:
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be larger than overlap")

    normalized = " ".join(text.split())
    chunks: list[DocumentChunk] = []
    start = 0
    i = 0
    while start < len(normalized):
        end = min(len(normalized), start + chunk_size)
        chunk = normalized[start:end].strip()
        if chunk:
            chunks.append(
                DocumentChunk(
                    chunk_id=f"{source}:{page or 0}:{i}",
                    source=source,
                    text=chunk,
                    page=page,
                )
            )
        if end == len(normalized):
            break
        start = end - overlap
        i += 1
    return chunks
