"""Tests for research bundle export."""
from __future__ import annotations

import json

from benchmarks.research_export import export_research_bundle
from config import Settings


def test_export_from_cache(tmp_path):
    settings = Settings()
    reports = settings.repo_root / "backend" / "reports"
    if not (reports / "benchmark_report.json").is_file():
        return  # skip if reports not generated locally

    out = tmp_path / "evaluation"
    paths = export_research_bundle(
        settings=settings,
        reports_dir=reports,
        out_root=out,
        run_id="test-run",
        from_cache=True,
        skip_cross_encoder=True,
    )
    assert paths["manifest"].is_file()
    assert paths["findings"].is_file()
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    assert manifest["run_id"] == "test-run"
    assert "studies" in manifest
    assert (out / "studies" / "01-embedding-strategies.md").is_file()
    assert (out / "artifacts" / "tables" / "table_all_methods.csv").is_file()
