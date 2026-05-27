#!/usr/bin/env python3
"""Quick smoke benchmark: 5 labeled queries, semantic vs soft embed."""
from __future__ import annotations

import json
from pathlib import Path

from config import Settings

from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot, load_eval_labels
from benchmarks.metrics import eval_rankings
from benchmarks.rank_utils import multimodal_score, rank_exhaustive, semantic_score


def main():
    settings = Settings()
    data_dir = settings.data_dir
    resumes = json.loads((data_dir / "cvs.json").read_text(encoding="utf-8"))
    jobs = json.loads((data_dir / "jobs.json").read_text(encoding="utf-8"))
    eval_map = load_eval_labels(data_dir / "eval_pairs.json")
    model_name = settings.embedding_model

    job_snaps = [job_to_snapshot(j, model_name) for j in jobs]
    cv_snaps = {r["id"]: cv_to_snapshot(r, model_name) for r in resumes}
    sample_qids = sorted(eval_map.keys())[:5]

    for label, fn in [
        ("Semantic cosine", lambda s: rank_exhaustive(s, job_snaps, lambda c, j: semantic_score(c, j, "cosine"))),
        (
            "Multimodal soft embed w=0.7",
            lambda s: rank_exhaustive(
                s,
                job_snaps,
                lambda c, j: multimodal_score(c, j, skills_mode="embedding", model_name=model_name),
            ),
        ),
    ]:
        ranked = {qid: fn(cv_snaps[qid]) for qid in sample_qids if qid in cv_snaps}
        subset = {qid: eval_map[qid] for qid in sample_qids if qid in eval_map}
        _, agg = eval_rankings(subset, ranked, top_k=5)
        print(f"{label}: nDCG@5={agg['avg_ndcg_at_k']:.3f} on {agg['queries']} queries")


if __name__ == "__main__":
    main()
