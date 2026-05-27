#!/usr/bin/env python3
"""Table 11 — fusion & constraint ablation (paper § advanced ML)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from config import Settings
from core.calibration import PlattCalibrator
from core.constraints import apply_constraints
from core.fusion import LearnedFusionModel, compute_hierarchical_multimodal
from core.scoring import compute_multimodal_weighted, compute_semantic

from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot, load_eval_labels
from benchmarks.metrics import eval_rankings
from benchmarks.rank_utils import rank_exhaustive, semantic_score


def _rank_fixed(cand, jobs, model_name):
    return rank_exhaustive(
        cand,
        jobs,
        lambda c, j: compute_multimodal_weighted(c, j, model_name=model_name),
    )


def _rank_hierarchical(cand, jobs, model_name):
    return rank_exhaustive(
        cand,
        jobs,
        lambda c, j: compute_hierarchical_multimodal(c, j, model_name=model_name),
    )


def _rank_learned(cand, jobs, model, model_name):
    return rank_exhaustive(
        cand,
        jobs,
        lambda c, j: model.score_pair(c, j, model_name=model_name),
    )


def _rank_constrained(cand, jobs, model_name):
    def fn(c, j):
        b = compute_multimodal_weighted(c, j, model_name=model_name)
        adj, _ = apply_constraints(b, c, j)
        return adj

    return rank_exhaustive(cand, jobs, fn)


def main():
    settings = Settings()
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-path", default=str(settings.data_dir / "eval_pairs.json"))
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--out", default=str(settings.repo_root / "backend" / "benchmark_outputs" / "table11_fusion.json"))
    args = parser.parse_args()

    resumes = json.loads(settings.cvs_path.read_text(encoding="utf-8"))
    jobs_raw = json.loads(settings.jobs_path.read_text(encoding="utf-8"))
    eval_map = load_eval_labels(args.eval_path)
    model_name = settings.embedding_model

    job_snaps = [job_to_snapshot(j, model_name) for j in jobs_raw]
    cv_snaps = {r["id"]: cv_to_snapshot(r, model_name) for r in resumes}

    fusion = LearnedFusionModel.load(settings.data_dir / "models" / "fusion.json")
    if fusion is None:
        from benchmarks.train_ml_models import build_training_matrix

        X, y, _ = build_training_matrix(settings)
        fusion = LearnedFusionModel.train(X, y)

    runners = {
        "Fixed multimodal α=0.7": lambda snap: _rank_fixed(snap, job_snaps, model_name),
        "Hierarchical skills": lambda snap: _rank_hierarchical(snap, job_snaps, model_name),
        "Learned fusion (LR)": lambda snap: _rank_learned(snap, job_snaps, fusion, model_name),
        "Multimodal + constraints": lambda snap: _rank_constrained(snap, job_snaps, model_name),
        "Semantic cosine": lambda snap: rank_exhaustive(
            snap, job_snaps, lambda c, j: semantic_score(c, j, "cosine")
        ),
    }

    summary = []
    for method, rank_fn in runners.items():
        ranked = {qid: rank_fn(cv_snaps[qid]) for qid in eval_map if qid in cv_snaps}
        _, agg = eval_rankings(eval_map, ranked, top_k=args.top_k)
        row = {"method": method, **agg}
        summary.append(row)
        print(f"{method:28} nDCG@5={agg['avg_ndcg_at_k']:.3f}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
