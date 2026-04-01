from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ingestion.pipeline import ingest_directory
from retrieval.index import HybridRetriever
from retrieval.reranker import CrossEncoderReranker


@dataclass(slots=True)
class Citation:
    id: str
    source: str
    page: int | None
    snippet: str


@dataclass(slots=True)
class RAGAnswer:
    answer: str
    citations: list[Citation]


class ProductionRAGAssistant:
    def __init__(self, docs_dir: Path):
        self.docs_dir = docs_dir
        self.chunks = ingest_directory(docs_dir)
        self.retriever = HybridRetriever(self.chunks)
        self.reranker = CrossEncoderReranker()

    def ask(self, question: str) -> RAGAnswer:
        retrieved = self.retriever.search(question, top_k=10, alpha=0.55)
        reranked = self.reranker.rerank(question, retrieved, top_k=5)

        bullets = [f"- {item.chunk.text[:220]}..." for item in reranked]
        answer = (
            "Grounded summary based on retrieved documents:\n"
            + "\n".join(bullets)
            + "\n\nNote: This answer is extractive and grounded in cited context."
        )

        citations = [
            Citation(
                id=item.chunk.chunk_id,
                source=item.chunk.source,
                page=item.chunk.page,
                snippet=item.chunk.text[:280],
            )
            for item in reranked
        ]
        return RAGAnswer(answer=answer, citations=citations)
