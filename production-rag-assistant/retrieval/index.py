from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from math import log, sqrt

from ingestion.types import DocumentChunk


@dataclass(slots=True)
class ScoredChunk:
    chunk: DocumentChunk
    bm25_score: float
    vector_score: float
    hybrid_score: float


class HybridRetriever:
    def __init__(self, chunks: list[DocumentChunk]):
        if not chunks:
            raise ValueError("No chunks provided")
        self.chunks = chunks
        self.tokens = [c.text.lower().split() for c in chunks]
        self.doc_freq = defaultdict(int)
        for toks in self.tokens:
            for term in set(toks):
                self.doc_freq[term] += 1
        self.avgdl = sum(len(toks) for toks in self.tokens) / len(self.tokens)
        self.tf = [Counter(toks) for toks in self.tokens]

    def search(self, query: str, top_k: int = 8, alpha: float = 0.5) -> list[ScoredChunk]:
        query_terms = query.lower().split()
        bm25_scores = [self._bm25_score(query_terms, i) for i in range(len(self.chunks))]
        vector_scores = [self._tfidf_cosine(query_terms, i) for i in range(len(self.chunks))]

        bm25_norm = _min_max_norm(bm25_scores)
        vector_norm = _min_max_norm(vector_scores)
        hybrid_scores = [alpha * b + (1 - alpha) * v for b, v in zip(bm25_norm, vector_norm)]

        top_indices = sorted(range(len(self.chunks)), key=lambda i: hybrid_scores[i], reverse=True)[:top_k]
        return [
            ScoredChunk(
                chunk=self.chunks[i],
                bm25_score=bm25_scores[i],
                vector_score=vector_scores[i],
                hybrid_score=hybrid_scores[i],
            )
            for i in top_indices
        ]

    def _bm25_score(self, query_terms: list[str], idx: int, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_len = len(self.tokens[idx])
        n_docs = len(self.tokens)
        for term in query_terms:
            f = self.tf[idx][term]
            if f == 0:
                continue
            n_qi = self.doc_freq.get(term, 0)
            idf = log((n_docs - n_qi + 0.5) / (n_qi + 0.5) + 1)
            denom = f + k1 * (1 - b + b * doc_len / self.avgdl)
            score += idf * (f * (k1 + 1)) / denom
        return score

    def _tfidf_cosine(self, query_terms: list[str], idx: int) -> float:
        n_docs = len(self.tokens)
        q_counts = Counter(query_terms)
        d_counts = self.tf[idx]
        terms = set(q_counts) | set(d_counts)

        q_vec = []
        d_vec = []
        for term in terms:
            df = self.doc_freq.get(term, 0) or 1
            idf = log((n_docs + 1) / (df + 1)) + 1
            q_vec.append(q_counts[term] * idf)
            d_vec.append(d_counts[term] * idf)

        dot = sum(a * b for a, b in zip(q_vec, d_vec))
        q_norm = sqrt(sum(a * a for a in q_vec))
        d_norm = sqrt(sum(b * b for b in d_vec))
        if q_norm == 0 or d_norm == 0:
            return 0.0
        return dot / (q_norm * d_norm)


def _min_max_norm(values: list[float]) -> list[float]:
    low = min(values)
    high = max(values)
    if low == high:
        return [0.0 for _ in values]
    return [(v - low) / (high - low) for v in values]
