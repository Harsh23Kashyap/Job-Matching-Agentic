"""Tests for lexical baselines and comparison table report."""
from __future__ import annotations

import csv
import json

import pytest

from benchmarks.baseline_strategies import build_all_strategies, build_lexical_baselines
from benchmarks.comparison import ComparisonBenchmark, write_comparison_report
from benchmarks.framework import BenchmarkFramework


@pytest.fixture(scope="module")
def corpus():
    fw = BenchmarkFramework(top_k=5)
    eval_map, resumes_by_id, _jobs_by_id, resumes, jobs = fw.load_corpus()
    cv_snaps, job_snaps = fw.build_snapshots(resumes, jobs, fw.settings.embedding_model)
    return eval_map, resumes_by_id, resumes, jobs, cv_snaps, job_snaps, fw.settings.embedding_model


def test_lexical_baseline_keys(corpus):
    _eval_map, resumes_by_id, _resumes, jobs, _cv_snaps, job_snaps, model_name = corpus
    baselines = build_lexical_baselines(jobs, resumes_by_id, job_snaps, model_name=model_name)
    assert {b.key for b in baselines} == {"bm25", "tfidf_cosine", "exact_skill_overlap"}


def test_build_all_strategies_includes_lexical_and_embedding(corpus):
    _eval_map, resumes_by_id, _resumes, jobs, _cv_snaps, job_snaps, model_name = corpus
    all_strategies = build_all_strategies(
        jobs,
        resumes_by_id,
        job_snaps,
        model_name=model_name,
        include_lexical_baselines=True,
    )
    keys = {s.key for s in all_strategies}
    assert "bm25" in keys
    assert "tfidf_cosine" in keys
    assert "exact_skill_overlap" in keys
    assert "semantic_cosine" in keys
    assert len(all_strategies) == 9


def test_comparison_table_format(tmp_path):
    bench = ComparisonBenchmark(top_k=5, include_lexical_baselines=True)
    report = bench.run()
    assert len(report.rows) == len(report.summary) * 5
    assert report.rows[0].keys() >= {"method", "metric", "top_k", "score", "latency_ms"}
    assert all(row["latency_ms"] >= 0 for row in report.rows)

    paths = write_comparison_report(report, tmp_path, prefix="test")
    rows = list(csv.DictReader(paths["table_csv"].open(encoding="utf-8")))
    assert rows[0]["metric"] in {"Precision@K", "Recall@K", "MRR", "nDCG@K", "MAP"}
    payload = json.loads(paths["table_json"].read_text(encoding="utf-8"))
    assert payload["meta"]["report_type"] == "lexical_vs_embedding_comparison"

    lexical = [s for s in report.summary if s["family"] == "lexical"]
    embedding = [s for s in report.summary if s["family"] == "embedding"]
    assert len(lexical) == 3
    assert len(embedding) == 6
    assert all(s["latency_ms"] < embedding[0]["latency_ms"] for s in lexical)
