from dataclasses import dataclass


@dataclass(slots=True)
class DocumentChunk:
    chunk_id: str
    source: str
    text: str
    page: int | None = None
