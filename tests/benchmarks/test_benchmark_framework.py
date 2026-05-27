"""Integration tests for the research benchmark framework."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from benchmarks.framework import BenchmarkFramework, write_report
from benchmarks.strategies import build_strategies


@pytest.fixture(scope="module")
def framework():
    return BenchmarkFramework(top_k=5)


def test_build_strategies_count(framework):
    eval_map, _, _, resumes, jobs = framework.load_corpus()
    cv_snaps, job_snaps = framework.build_snapshots(resumes, jobs, framework.settings.embedding_model)
    strategies = build_strategies(job_snaps, model_name=framework.settings.embedding_model)
    assert len(strategies) == 6
    keys = {s.key for s in strategies}
    assert keys == {
        "semantic_cosine",
        "semantic_euclidean",
        "skills_jaccard",
        "soft_skill_embed",
        "multimodal_weighted",
        "rrf_ensemble",
    }
    assert len(eval_map) == 30


def test_framework_run_and_write(tmp_path, framework):
    report = framework.run()
    assert len(report.summary) == 6
    assert report.meta["top_k"] == 5
    for row in report.summary:
        assert 0.0 <= row["ndcg_at_k"] <= 1.0
        assert 0.0 <= row["mrr"] <= 1.0
        assert row["queries"] == report.meta["corpus"]["labeled_queries"]

    paths = write_report(report, tmp_path, prefix="test")
    assert paths["json"].is_file()
    payload = json.loads(paths["json"].read_text(encoding="utf-8"))
    assert "summary" in payload and len(payload["summary"]) == 6
    assert paths["summary_csv"].read_text(encoding="utf-8").startswith("method_key")
    assert paths["per_query_csv"].is_file()
