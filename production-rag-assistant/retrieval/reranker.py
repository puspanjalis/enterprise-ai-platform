from __future__ import annotations

from typing import Iterable

from retrieval.index import ScoredChunk


class CrossEncoderReranker:
    """
    Uses sentence-transformers CrossEncoder when available,
    otherwise falls back to token-overlap scoring.
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = None
        try:
            from sentence_transformers import CrossEncoder

            self.model = CrossEncoder(model_name)
        except Exception:
            self.model = None

    def rerank(self, query: str, candidates: Iterable[ScoredChunk], top_k: int = 5) -> list[ScoredChunk]:
        items = list(candidates)
        if not items:
            return []

        if self.model is not None:
            pairs = [(query, item.chunk.text) for item in items]
            scores = self.model.predict(pairs)
        else:
            q = set(query.lower().split())
            scores = [
                len(q.intersection(set(item.chunk.text.lower().split()))) / (len(q) + 1)
                for item in items
            ]

        rescored = sorted(
            zip(items, scores, strict=False),
            key=lambda row: (float(row[1]), row[0].hybrid_score),
            reverse=True,
        )
        return [item for item, _ in rescored[:top_k]]
