#!/usr/bin/env python3
"""Phase 1.1 ANN benchmark — pool=10 shortlist, rerank, latency table (Table 10)."""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import time
from pathlib import Path

import numpy as np

from config import Settings
from core.scoring import compute_multimodal_weighted, compute_semantic

from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot, load_eval_labels
from benchmarks.metrics import ndcg_at_k, precision_at_k, recall_at_k
from stores.factory import create_store

SUPPORTED_STRATEGIES = ["semantic", "multimodal"]
SUPPORTED_METRICS = ["cosine", "euclidean"]


def p95(values: list[float]) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    idx = int(0.95 * (len(sorted_vals) - 1))
    return sorted_vals[idx]


def score_pair(candidate_snap, job_snap, strategy, metric, semantic_weight, model_name):
    if strategy == "multimodal":
        return compute_multimodal_weighted(
            candidate_snap,
            job_snap,
            metric=metric,
            semantic_weight=semantic_weight,
            skills_mode="jaccard",
            model_name=model_name,
        )
    return compute_semantic(candidate_snap, job_snap, metric)


def evaluate_config(
    *,
    store_name: str,
    strategy: str,
    metric: str,
    semantic_weight: float,
    chroma_space: str | None,
    collection_suffix: str,
    top_k: int,
    candidate_pool: int,
    repeats: int,
    eval_map,
    cv_snaps,
    job_snaps_by_id,
    settings: Settings,
    model_name: str,
):
    prev_store = settings.vector_store
    settings.vector_store = store_name
    store = create_store(
        settings,
        "jobs_collection",
        collection_suffix=collection_suffix,
        chroma_space=chroma_space or "cosine",
    )
    for job in job_snaps_by_id.values():
        store.upsert(
            job.id,
            np.asarray(job.embedding, dtype=np.float32),
            {"id": job.id, "title": job.title},
        )

    query_ids = [qid for qid in eval_map if qid in cv_snaps]
    per_query_rows = []

    for repeat in range(1, repeats + 1):
        for query_id in query_ids:
            cand = cv_snaps[query_id]
            relevance_map = eval_map[query_id]
            relevant_ids = {d for d, r in relevance_map.items() if r > 0}
            vec = np.asarray(cand.embedding, dtype=np.float32)

            t0 = time.perf_counter()
            hits = store.search(vec, k=candidate_pool)
            latency_ms = (time.perf_counter() - t0) * 1000.0

            reranked = []
            for hit in hits:
                job_snap = job_snaps_by_id.get(hit.entity_id)
                if job_snap is None:
                    continue
                breakdown = score_pair(
                    cand,
                    job_snap,
                    strategy,
                    metric,
                    semantic_weight,
                    model_name,
                )
                reranked.append((hit.entity_id, breakdown.final_score))
            reranked.sort(key=lambda x: x[1], reverse=True)
            predicted = [doc_id for doc_id, _ in reranked[:top_k]]

            per_query_rows.append(
                {
                    "repeat": repeat,
                    "query_id": query_id,
                    "store": store_name,
                    "strategy": strategy,
                    "metric": metric,
                    "semantic_weight": semantic_weight if strategy == "multimodal" else None,
                    "skills_weight": (1.0 - semantic_weight) if strategy == "multimodal" else None,
                    "chroma_space": chroma_space if store_name == "chroma" else None,
                    "top_k": top_k,
                    "candidate_pool": candidate_pool,
                    "latency_ms": latency_ms,
                    "precision_at_k": precision_at_k(predicted, relevant_ids, top_k),
                    "recall_at_k": recall_at_k(predicted, relevant_ids, top_k),
                    "ndcg_at_k": ndcg_at_k(predicted, relevance_map, top_k),
                }
            )

    settings.vector_store = prev_store
    summary = {
        "store": store_name,
        "strategy": strategy,
        "metric": metric,
        "semantic_weight": semantic_weight if strategy == "multimodal" else None,
        "chroma_space": chroma_space if store_name == "chroma" else None,
        "top_k": top_k,
        "candidate_pool": candidate_pool,
        "repeats": repeats,
        "queries": len(query_ids),
        "avg_precision_at_k": statistics.mean(r["precision_at_k"] for r in per_query_rows),
        "avg_recall_at_k": statistics.mean(r["recall_at_k"] for r in per_query_rows),
        "avg_ndcg_at_k": statistics.mean(r["ndcg_at_k"] for r in per_query_rows),
        "avg_latency_ms": statistics.mean(r["latency_ms"] for r in per_query_rows),
        "p95_latency_ms": p95([r["latency_ms"] for r in per_query_rows]),
    }
    return summary, per_query_rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    settings = Settings()
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-path", default=str(settings.data_dir / "eval_pairs.json"))
    parser.add_argument("--data-dir", default=str(settings.data_dir))
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--candidate-pool", type=int, default=10)
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--stores", nargs="+", default=["chroma"])
    parser.add_argument("--chroma-spaces", nargs="+", default=["cosine", "l2"])
    parser.add_argument("--multimodal-weights", nargs="+", type=float, default=[0.8, 0.7, 0.6, 0.5])
    parser.add_argument("--skip-qdrant", action="store_true")
    parser.add_argument("--out-dir", default=str(settings.repo_root / "backend" / "benchmark_outputs"))
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    resumes = json.loads((data_dir / "cvs.json").read_text(encoding="utf-8"))
    jobs = json.loads((data_dir / "jobs.json").read_text(encoding="utf-8"))
    eval_map = load_eval_labels(args.eval_path)
    model_name = settings.embedding_model

    job_snaps_by_id = {j["id"]: job_to_snapshot(j, model_name) for j in jobs}
    cv_snaps = {r["id"]: cv_to_snapshot(r, model_name) for r in resumes}

    stores = list(args.stores)
    if args.skip_qdrant and "qdrant" in stores:
        stores.remove("qdrant")

    summary_rows: list[dict] = []
    per_query_rows: list[dict] = []

    for store in stores:
        if store == "chroma":
            param_sets = [{"chroma_space": space, "suffix": f"_phase11_{space}"} for space in args.chroma_spaces]
        elif store == "qdrant":
            param_sets = [{"chroma_space": None, "suffix": "_phase11_qdrant"}]
        else:
            continue

        for params in param_sets:
            for strategy in SUPPORTED_STRATEGIES:
                for metric in SUPPORTED_METRICS:
                    weights = args.multimodal_weights if strategy == "multimodal" else [0.7]
                    for semantic_weight in weights:
                        try:
                            summary, rows = evaluate_config(
                                store_name=store,
                                strategy=strategy,
                                metric=metric,
                                semantic_weight=semantic_weight,
                                chroma_space=params["chroma_space"],
                                collection_suffix=params["suffix"],
                                top_k=args.top_k,
                                candidate_pool=args.candidate_pool,
                                repeats=args.repeats,
                                eval_map=eval_map,
                                cv_snaps=cv_snaps,
                                job_snaps_by_id=job_snaps_by_id,
                                settings=settings,
                                model_name=model_name,
                            )
                            summary_rows.append(summary)
                            per_query_rows.extend(rows)
                            w = f" w={semantic_weight:.2f}" if strategy == "multimodal" else ""
                            print(
                                f"[OK] {store} {strategy}/{metric}{w} "
                                f"nDCG={summary['avg_ndcg_at_k']:.3f} "
                                f"lat={summary['avg_latency_ms']:.2f}ms"
                            )
                        except Exception as exc:
                            print(f"[SKIP] {store} {strategy}/{metric} — {exc}")

    out_dir = Path(args.out_dir)
    write_csv(out_dir / "phase11_summary.csv", summary_rows)
    write_csv(out_dir / "phase11_per_query.csv", per_query_rows)
    print(f"\nWrote {out_dir / 'phase11_summary.csv'} ({len(summary_rows)} configs)")


if __name__ == "__main__":
    main()
