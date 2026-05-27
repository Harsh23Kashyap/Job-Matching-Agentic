"""Tests for composite scoring evaluation."""
from __future__ import annotations

from benchmarks.composite_eval import CompositeEval, write_composite_report
from config import Settings


def test_composite_eval_runs_on_demo_corpus():
    settings = Settings()
    eval_ = CompositeEval(settings=settings, top_k=5)
    report = eval_.run()
    assert report.summary["method_key"] == "composite"
    assert 0.0 <= report.summary["ndcg_at_k"] <= 1.0
    assert len(report.per_query) == report.meta["corpus"]["labeled_queries"]
    assert report.meta["strategy"] == "composite"


def test_write_composite_report(tmp_path):
    settings = Settings()
    report = CompositeEval(settings=settings, top_k=5).run()
    paths = write_composite_report(report, tmp_path, prefix="composite")
    assert paths["json"].is_file()
    assert paths["summary_csv"].is_file()
    assert paths["per_query_csv"].is_file()
