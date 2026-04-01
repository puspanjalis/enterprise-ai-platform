from eval.run_eval import run_eval


def test_eval_metrics_above_threshold() -> None:
    retrieval_recall, grounded_answer_score = run_eval()

    assert retrieval_recall >= 0.8
    assert grounded_answer_score >= 0.7
