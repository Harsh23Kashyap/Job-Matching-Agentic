from benchmarks.metrics import (
    aggregate_query_metrics,
    average_precision,
    dcg_at_k,
    eval_rankings,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
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
    assert summary["avg_mrr"] > 0
    assert summary["avg_map"] > 0
    assert per_query[0]["mrr"] == 1.0
    agg = aggregate_query_metrics(per_query)
    assert agg["queries"] == 2
    assert "avg_mrr" in agg
    assert "avg_map" in agg


def test_reciprocal_rank_and_map():
    pred = ["x", "doc_a", "doc_b"]
    relevant = {"doc_a", "doc_b"}
    assert reciprocal_rank(pred, relevant) == 0.5
    assert average_precision(pred, relevant) > 0
    assert reciprocal_rank(["x", "y"], relevant) == 0.0
    assert average_precision(["x", "y"], relevant) == 0.0
