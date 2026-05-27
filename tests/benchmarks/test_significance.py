"""Tests for paired bootstrap significance testing."""
from __future__ import annotations

import json

import pytest

from benchmarks.significance import (
    bootstrap_mean_ci,
    paired_bootstrap_ndcg,
    paired_bootstrap_test,
    run_significance_analysis,
    write_significance_report,
)


def test_bootstrap_mean_ci_deterministic():
    values = [0.5, 0.6, 0.7, 0.8, 0.9]
    a = bootstrap_mean_ci(values, n_resamples=1000, seed=7)
    b = bootstrap_mean_ci(values, n_resamples=1000, seed=7)
    assert a == b
    assert a["mean"] == pytest.approx(0.7)
    assert a["ci95_lo"] <= a["mean"] <= a["ci95_hi"]


def test_paired_bootstrap_clear_winner():
    baseline = {f"q{i}": 0.2 for i in range(10)}
    compare = {f"q{i}": 0.8 for i in range(10)}
    result = paired_bootstrap_test(baseline, compare, n_resamples=2000, seed=1)
    assert result["wins"] == 10
    assert result["losses"] == 0
    assert result["ties"] == 0
    assert result["mean_diff"] == pytest.approx(0.6)
    assert result["p_value"] == 0.0
    assert result["significant_at_05"] is True
    assert result["ci95_lo"] > 0


def test_paired_bootstrap_ties():
    baseline = {"q1": 0.5, "q2": 0.5}
    compare = {"q1": 0.5, "q2": 0.5}
    result = paired_bootstrap_test(baseline, compare, n_resamples=500, seed=3)
    assert result["wins"] == 0
    assert result["losses"] == 0
    assert result["ties"] == 2
    assert result["mean_diff"] == pytest.approx(0.0)


def test_paired_bootstrap_ndcg_compat():
    per_query = [
        {"method": "A", "query_id": "q1", "ndcg_at_k": 0.4},
        {"method": "B", "query_id": "q1", "ndcg_at_k": 0.9},
        {"method": "A", "query_id": "q2", "ndcg_at_k": 0.3},
        {"method": "B", "query_id": "q2", "ndcg_at_k": 0.8},
    ]
    sig = paired_bootstrap_ndcg(per_query, "A", "B", n_resamples=1000, seed=5)
    assert sig["baseline"] == "A"
    assert sig["compare"] == "B"
    assert sig["mean_ndcg_diff"] > 0
    assert "p_value" in sig
    assert sig["wins"] == 2


def test_run_significance_and_write(tmp_path):
    per_query = []
    for method_key, method, ndcg_vals in (
        ("base", "Baseline", [0.5, 0.6, 0.55, 0.52]),
        ("better", "Better", [0.7, 0.75, 0.72, 0.71]),
        ("mixed", "Mixed", [0.6, 0.4, 0.65, 0.58]),
    ):
        for i, ndcg in enumerate(ndcg_vals):
            per_query.append(
                {
                    "method_key": method_key,
                    "method": method,
                    "query_id": f"q{i + 1}",
                    "ndcg_at_k": ndcg,
                    "mrr": ndcg * 0.9,
                    "precision_at_k": ndcg,
                    "recall_at_k": ndcg,
                    "map": ndcg,
                }
            )

    report = run_significance_analysis(
        per_query,
        baseline_key="base",
        n_resamples=1000,
        seed=11,
        top_k=5,
    )
    assert len(report.methods) == 3
    assert len(report.comparisons) == 4  # 2 compares × 2 metrics

    better_ndcg = next(
        r for r in report.comparisons if r["compare_key"] == "better" and r["metric"] == "ndcg_at_k"
    )
    assert better_ndcg["wins"] + better_ndcg["losses"] + better_ndcg["ties"] == 4
    assert "mean" in report.methods[0]["metrics"]["ndcg_at_k"]

    paths = write_significance_report(report, tmp_path, prefix="test")
    payload = json.loads(paths["json"].read_text(encoding="utf-8"))
    assert payload["meta"]["report_type"] == "bootstrap_significance"
    assert "comparisons" in payload
    md = paths["markdown"].read_text(encoding="utf-8")
    assert "Bootstrap Significance" in md
    assert "W/L/T" in md
