"""Tests for research pipeline orchestration."""
from __future__ import annotations

from pathlib import Path

from benchmarks.research_pipeline import PipelineConfig, make_run_dir, run_research_pipeline
from config import Settings


def test_make_run_dir_uses_prefix():
    path = make_run_dir(Path("/tmp/reports"), "research_run_test123")
    assert path.name == "research_run_test123"


def test_pipeline_stops_on_validation_failure(tmp_path):
    settings = Settings()
    bad_dir = tmp_path / "bad_data"
    bad_dir.mkdir()
    (bad_dir / "cvs.json").write_text("[]", encoding="utf-8")
    (bad_dir / "jobs.json").write_text("[]", encoding="utf-8")
    (bad_dir / "eval_pairs.json").write_text('{"labels": []}', encoding="utf-8")

    run_dir = tmp_path / "research_run_fail"
    config = PipelineConfig(
        settings=settings,
        run_dir=run_dir,
        data_dir=bad_dir,
        eval_path=bad_dir / "eval_pairs.json",
        profiles_path=bad_dir / "fairness_audit_profiles.json",
        skip_cross_encoder=True,
    )
    result = run_research_pipeline(config)
    assert result.valid is False
    assert len(result.steps) == 1
    assert result.steps[0].name == "dataset_validation"
    assert (run_dir / "dataset_validation.json").is_file()
    assert (run_dir / "pipeline_manifest.json").is_file()
