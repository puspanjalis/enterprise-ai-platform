from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.rag_service import ProductionRAGAssistant


def run_eval() -> tuple[float, float]:
    root = Path(__file__).resolve().parents[1]
    assistant = ProductionRAGAssistant(root / "data")
    dataset = json.loads((root / "eval" / "eval_dataset.json").read_text(encoding="utf-8"))

    retrieval_hits = 0
    answer_hits = 0

    for item in dataset:
        response = assistant.ask(item["question"])
        sources = {c.source for c in response.citations}
        if item["source"] in sources:
            retrieval_hits += 1

        answer_lower = response.answer.lower()
        if all(token.lower() in answer_lower for token in item["must_contain"]):
            answer_hits += 1

    retrieval_recall = retrieval_hits / len(dataset)
    grounded_answer_score = answer_hits / len(dataset)
    return retrieval_recall, grounded_answer_score


def main() -> None:
    retrieval_recall, grounded_answer_score = run_eval()
    print(f"retrieval_recall={retrieval_recall:.2f}")
    print(f"grounded_answer_score={grounded_answer_score:.2f}")

    min_recall = 0.8
    min_grounded_score = 0.7

    if retrieval_recall < min_recall or grounded_answer_score < min_grounded_score:
        raise SystemExit(
            f"Evaluation gate failed. recall={retrieval_recall:.2f}, grounded={grounded_answer_score:.2f}"
        )


if __name__ == "__main__":
    main()
