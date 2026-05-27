#!/usr/bin/env python3
"""Paper progression benchmark: lexical → semantic → multimodal → RRF → cross-encoder."""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import statistics
from collections import defaultdict
from pathlib import Path

from config import Settings
from core.cross_encoder_rerank import rerank_jobs
from core.embedding import get_model, reset_embedding_cache
from core.lexical import LexicalRanker

from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot, load_eval_labels
from benchmarks.metrics import eval_rankings
from benchmarks.rank_utils import multimodal_score, rank_exhaustive, rrf_fuse_lists, semantic_score
from benchmarks.significance import paired_bootstrap_ndcg


def _run_config(name, eval_map, cv_snaps, job_snaps, jobs_raw, top_k, rank_fn):
    ranked = {qid: rank_fn(cv_snaps[qid]) for qid in eval_map if qid in cv_snaps}
    per_q, agg = eval_rankings(eval_map, ranked, top_k)
    row = {"method": name, **agg}
    for r in per_q:
        r["method"] = name
    return row, per_q


def main():
    settings = Settings()
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-path", default=str(settings.data_dir / "eval_pairs.json"))
    parser.add_argument("--data-dir", default=str(settings.data_dir))
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--rerank-pool", type=int, default=10)
    parser.add_argument("--skip-cross-encoder", action="store_true")
    parser.add_argument("--skip-alt-embedder", action="store_true")
    parser.add_argument("--out-dir", default=str(settings.repo_root / "backend" / "benchmark_outputs"))
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    resumes = json.loads((data_dir / "cvs.json").read_text(encoding="utf-8"))
    jobs = json.loads((data_dir / "jobs.json").read_text(encoding="utf-8"))
    eval_map = load_eval_labels(args.eval_path)
    jobs_by_id = {j["id"]: j for j in jobs}
    resumes_by_id = {r["id"]: r for r in resumes}
    model_name = settings.embedding_model

    print(f"Corpus: {len(resumes)} resumes, {len(jobs)} jobs")
    print(f"Embedding model: {model_name}\n")

    job_snaps = [job_to_snapshot(j, model_name) for j in jobs]
    cv_snaps = {r["id"]: cv_to_snapshot(r, model_name) for r in resumes}

    summary: list[dict] = []
    per_query_all: list[dict] = []

    def add(name, rank_fn):
        row, per_q = _run_config(name, eval_map, cv_snaps, job_snaps, jobs, args.top_k, rank_fn)
        summary.append(row)
        per_query_all.extend(per_q)
        print(
            f"{name:42} P@5={row['avg_precision_at_k']:.3f} "
            f"R@5={row['avg_recall_at_k']:.3f} nDCG@5={row['avg_ndcg_at_k']:.3f}"
        )

    ranker = LexicalRanker(jobs)
    add("TF-IDF (lexical)", lambda snap: ranker.rank_jobs(resumes_by_id[snap.id], "tfidf", top_k=len(jobs)))
    add("BM25 (lexical)", lambda snap: ranker.rank_jobs(resumes_by_id[snap.id], "bm25", top_k=len(jobs)))

    add("Semantic cosine", lambda snap: rank_exhaustive(snap, job_snaps, lambda c, j: semantic_score(c, j, "cosine")))
    add(
        "Multimodal Jaccard w=0.7",
        lambda snap: rank_exhaustive(
            snap,
            job_snaps,
            lambda c, j: multimodal_score(c, j, skills_mode="jaccard", model_name=model_name),
        ),
    )
    add(
        "Multimodal soft embed w=0.7",
        lambda snap: rank_exhaustive(
            snap,
            job_snaps,
            lambda c, j: multimodal_score(c, j, skills_mode="embedding", model_name=model_name),
        ),
    )

    def rrf_rank(snap):
        sem = rank_exhaustive(snap, job_snaps, lambda c, j: semantic_score(c, j, "cosine"))
        mm = rank_exhaustive(
            snap,
            job_snaps,
            lambda c, j: multimodal_score(c, j, skills_mode="jaccard", model_name=model_name),
        )
        soft = rank_exhaustive(
            snap,
            job_snaps,
            lambda c, j: multimodal_score(c, j, skills_mode="embedding", model_name=model_name),
        )
        euc = rank_exhaustive(
            snap,
            job_snaps,
            lambda c, j: multimodal_score(c, j, metric="euclidean", skills_mode="jaccard", model_name=model_name),
        )
        return rrf_fuse_lists([sem, mm, soft, euc], k=settings.rrf_k)

    add("RRF ensemble (4 lists)", rrf_rank)

    os.environ["BENCHMARK_RICH_TEMPLATES"] = "1"
    reset_embedding_cache()
    rich_jobs = [job_to_snapshot(j, model_name) for j in jobs]
    rich_cv = {r["id"]: cv_to_snapshot(r, model_name) for r in resumes}
    add(
        "Semantic cosine (rich templates)",
        lambda snap: rank_exhaustive(rich_cv[snap.id], rich_jobs, lambda c, j: semantic_score(c, j, "cosine")),
    )
    os.environ.pop("BENCHMARK_RICH_TEMPLATES", None)
    reset_embedding_cache()

    if not args.skip_cross_encoder:
        pool = min(args.rerank_pool, len(jobs))

        def ce_rank(snap):
            base = rank_exhaustive(
                snap,
                job_snaps,
                lambda c, j: multimodal_score(c, j, skills_mode="embedding", model_name=model_name),
            )
            shortlist = [jobs_by_id[jid] for jid, _ in base[:pool]]
            priors = {jid: sc for jid, sc in base}
            return rerank_jobs(resumes_by_id[snap.id], shortlist, prior_scores=priors)

        add(f"Soft embed + cross-encoder (pool={pool})", ce_rank)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = out_dir / "paper_progression_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    sig = paired_bootstrap_ndcg(per_query_all, "Semantic cosine", "Multimodal soft embed w=0.7")
    (out_dir / "paper_bootstrap_significance.json").write_text(json.dumps(sig, indent=2), encoding="utf-8")

    print(f"\nWrote {summary_path}")
    print(f"Bootstrap nDCG diff: {sig['mean_ndcg_diff']:.4f} CI [{sig['ci95_lo']:.4f}, {sig['ci95_hi']:.4f}]")


if __name__ == "__main__":
    main()
