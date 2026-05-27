"""Shared IR metrics for offline benchmarks."""
from __future__ import annotations

import math
import statistics
from collections import defaultdict


def precision_at_k(pred_ids, relevant_ids, k):
    top = pred_ids[:k]
    if not top or k <= 0:
        return 0.0
    return sum(1 for d in top if d in relevant_ids) / float(k)


def recall_at_k(pred_ids, relevant_ids, k):
    if not relevant_ids:
        return 0.0
    return sum(1 for d in pred_ids[:k] if d in relevant_ids) / float(len(relevant_ids))


def dcg_at_k(pred_ids, relevance_map, k):
    score = 0.0
    for rank, doc_id in enumerate(pred_ids[:k], start=1):
        rel = relevance_map.get(doc_id, 0)
        if rel <= 0:
            continue
        score += (2**rel - 1) / math.log2(rank + 1)
    return score


def ndcg_at_k(pred_ids, relevance_map, k):
    if not relevance_map:
        return 0.0
    ideal = [d for d, _ in sorted(relevance_map.items(), key=lambda x: x[1], reverse=True)]
    ideal_dcg = dcg_at_k(ideal, relevance_map, k)
    if ideal_dcg == 0:
        return 0.0
    return dcg_at_k(pred_ids, relevance_map, k) / ideal_dcg


def aggregate_query_metrics(per_query: list[dict]) -> dict:
    return {
        "avg_precision_at_k": statistics.mean(r["precision_at_k"] for r in per_query),
        "avg_recall_at_k": statistics.mean(r["recall_at_k"] for r in per_query),
        "avg_ndcg_at_k": statistics.mean(r["ndcg_at_k"] for r in per_query),
        "queries": len(per_query),
    }


def eval_rankings(eval_map, ranked_by_query: dict[str, list[tuple[str, float]]], top_k: int):
    per_query = []
    for qid, relevance_map in eval_map.items():
        if qid not in ranked_by_query:
            continue
        relevant = {d for d, r in relevance_map.items() if r > 0}
        pred = [d for d, _ in ranked_by_query[qid][:top_k]]
        per_query.append(
            {
                "query_id": qid,
                "precision_at_k": precision_at_k(pred, relevant, top_k),
                "recall_at_k": recall_at_k(pred, relevant, top_k),
                "ndcg_at_k": ndcg_at_k(pred, relevance_map, top_k),
                "predicted_ids": pred,
            }
        )
    return per_query, aggregate_query_metrics(per_query)
