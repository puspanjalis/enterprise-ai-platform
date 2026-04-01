from pathlib import Path

from app.rag_service import ProductionRAGAssistant


def test_grounded_answer_includes_citations() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    rag = ProductionRAGAssistant(base_dir / "data")

    response = rag.ask("What is the incident response SLA?")

    assert response.citations, "Expected at least one citation"
    assert any(c.source == "operations_handbook.md" for c in response.citations)
    assert "grounded" in response.answer.lower()
