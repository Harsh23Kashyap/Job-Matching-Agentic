from benchmarks.metrics import (
    aggregate_query_metrics,
    dcg_at_k,
    eval_rankings,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
)


def test_precision_and_recall_at_k():
    pred = ["a", "b", "c", "d"]
    relevant = {"a", "c"}
    assert precision_at_k(pred, relevant, 2) == 0.5
    assert recall_at_k(pred, relevant, 4) == 1.0
    assert precision_at_k([], relevant, 3) == 0.0


def test_ndcg_perfect_ranking():
    relevance = {"a": 3, "b": 2, "c": 1}
    pred = ["a", "b", "c"]
    assert ndcg_at_k(pred, relevance, 3) == 1.0
    assert dcg_at_k(pred, relevance, 3) > 0


def test_eval_rankings_aggregate():
    eval_map = {
        "q1": {"doc_a": 2, "doc_b": 1},
        "q2": {"doc_x": 1},
    }
    ranked = {
        "q1": [("doc_a", 0.9), ("doc_c", 0.1)],
        "q2": [("doc_x", 0.5)],
    }
    per_query, summary = eval_rankings(eval_map, ranked, top_k=2)
    assert len(per_query) == 2
    assert summary["queries"] == 2
    assert summary["avg_precision_at_k"] > 0
    agg = aggregate_query_metrics(per_query)
    assert agg["queries"] == 2
