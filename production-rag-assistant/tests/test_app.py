from pathlib import Path

from core.rag_engine import answer, load_documents


def test_answer_returns_citation() -> None:
    data_dir = Path(__file__).resolve().parents[1] / 'data'
    chunks = load_documents(data_dir)
    result = answer('What is the mitigation timeline for P1 incidents?', chunks)
    assert result['citations']
    assert '4 hours' in result['answer']
