"""Tests for paper table generation."""
from __future__ import annotations

import json
from pathlib import Path

from benchmarks.paper_tables.generators import generate_all_paper_tables
from config import Settings


def test_generate_paper_tables_from_reports(tmp_path):
    settings = Settings()
    reports = settings.repo_root / "backend" / "reports"
    if not (reports / "comparison_summary.json").is_file():
        return

    out = tmp_path / "paper_tables"
    result = generate_all_paper_tables(
        reports_dir=reports,
        out_dir=out,
        data_dir=settings.data_dir,
        top_k=5,
    )
    assert (out / "README.md").is_file()
    assert (out / "manifest.json").is_file()
    assert (out / "table1_method_comparison.md").is_file()
    assert (out / "table1_method_comparison.tex").is_file()
    md = (out / "table1_method_comparison.md").read_text(encoding="utf-8")
    assert "tab:method-comparison" in md
    assert "nDCG@5" in md

    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["top_k"] == 5
    assert "method_comparison" in manifest["tables"]
