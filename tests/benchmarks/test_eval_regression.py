"""Regression gate against expected benchmark outputs (Table 9 subset)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from config import Settings
from core.lexical import LexicalRanker

from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot, load_eval_labels
from benchmarks.metrics import eval_rankings
from benchmarks.rank_utils import multimodal_score, rank_exhaustive, semantic_score

TOLERANCE = 0.04
EXPECTED_PATH = Path(__file__).resolve().parents[2] / "data" / "expected" / "paper_progression_summary.json"


@pytest.fixture(scope="module")
def eval_corpus():
    settings = Settings()
    data_dir = settings.data_dir
    resumes = json.loads((data_dir / "cvs.json").read_text(encoding="utf-8"))
    jobs = json.loads((data_dir / "jobs.json").read_text(encoding="utf-8"))
    eval_map = load_eval_labels(data_dir / "eval_pairs.json")
    model_name = settings.embedding_model
    job_snaps = [job_to_snapshot(j, model_name) for j in jobs]
    cv_snaps = {r["id"]: cv_to_snapshot(r, model_name) for r in resumes}
    resumes_by_id = {r["id"]: r for r in resumes}
    return eval_map, cv_snaps, job_snaps, jobs, resumes_by_id, model_name


@pytest.mark.skipif(not EXPECTED_PATH.is_file(), reason="expected summary missing")
def test_paper_progression_regression(eval_corpus):
    eval_map, cv_snaps, job_snaps, jobs, resumes_by_id, model_name = eval_corpus
    expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
    expected_by_method = {row["method"]: row for row in expected}

    ranker = LexicalRanker(jobs)
    runners = {
        "TF-IDF (lexical)": lambda snap: ranker.rank_jobs(resumes_by_id[snap.id], "tfidf", top_k=len(jobs)),
        "BM25 (lexical)": lambda snap: ranker.rank_jobs(resumes_by_id[snap.id], "bm25", top_k=len(jobs)),
        "Semantic cosine": lambda snap: rank_exhaustive(snap, job_snaps, lambda c, j: semantic_score(c, j, "cosine")),
        "Multimodal Jaccard w=0.7": lambda snap: rank_exhaustive(
            snap,
            job_snaps,
            lambda c, j: multimodal_score(c, j, skills_mode="jaccard", model_name=model_name),
        ),
        "Multimodal soft embed w=0.7": lambda snap: rank_exhaustive(
            snap,
            job_snaps,
            lambda c, j: multimodal_score(c, j, skills_mode="embedding", model_name=model_name),
        ),
    }

    for method, rank_fn in runners.items():
        if method not in expected_by_method:
            continue
        ranked = {qid: rank_fn(cv_snaps[qid]) for qid in eval_map if qid in cv_snaps}
        _, agg = eval_rankings(eval_map, ranked, top_k=5)
        exp = expected_by_method[method]
        assert abs(agg["avg_ndcg_at_k"] - exp["avg_ndcg_at_k"]) <= TOLERANCE, method
