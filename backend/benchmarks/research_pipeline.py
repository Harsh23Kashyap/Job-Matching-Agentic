"""Orchestrate the full offline research evaluation pipeline."""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from config import Settings

from benchmarks.ablation import AblationStudy, print_ablation_summary, write_ablation_report
from benchmarks.comparison import ComparisonBenchmark, print_comparison_table, write_comparison_report
from benchmarks.composite_eval import CompositeEval, print_composite_summary, write_composite_report
from benchmarks.cross_encoder_report import print_report as print_cross_encoder_report
from benchmarks.cross_encoder_report import run_report as run_cross_encoder_report
from benchmarks.cross_encoder_report import write_report as write_cross_encoder_report
from benchmarks.dataset_validation import validate_eval_corpus, write_validation_report
from benchmarks.explainability_eval import ExplainabilityEval, print_explainability_summary, write_explainability_report
from benchmarks.fairness_audit import FairnessAudit, print_fairness_audit_summary, write_fairness_audit_report
from benchmarks.paper_tables.generators import generate_all_paper_tables
from benchmarks.significance import (
    DEFAULT_N_RESAMPLES,
    DEFAULT_SEED,
    print_significance_summary,
    run_significance_analysis,
    write_significance_report,
)


@dataclass
class StepResult:
    name: str
    status: str  # ok | skipped | failed
    duration_sec: float
    outputs: dict[str, str] = field(default_factory=dict)
    error: str | None = None


@dataclass
class PipelineConfig:
    settings: Settings
    run_dir: Path
    data_dir: Path
    eval_path: Path
    profiles_path: Path
    top_k: int = 5
    n_resamples: int = DEFAULT_N_RESAMPLES
    seed: int = DEFAULT_SEED
    skip_cross_encoder: bool = False
    enable_cross_encoder: bool | None = None


@dataclass
class PipelineResult:
    run_id: str
    run_dir: Path
    manifest_path: Path
    steps: list[StepResult]
    valid: bool


def _cross_encoder_enabled(config: PipelineConfig) -> bool:
    if config.skip_cross_encoder:
        return False
    if config.enable_cross_encoder is not None:
        return config.enable_cross_encoder
    env = os.environ.get("ENABLE_CROSS_ENCODER_RERANK", "").lower()
    if env in {"1", "true", "yes"}:
        return True
    return bool(config.settings.enable_cross_encoder_rerank)


def _step(name: str, fn: Callable[[], dict[str, str]]) -> StepResult:
    t0 = time.perf_counter()
    try:
        outputs = fn()
        return StepResult(name=name, status="ok", duration_sec=round(time.perf_counter() - t0, 3), outputs=outputs)
    except Exception as exc:  # noqa: BLE001 - pipeline must capture failures for the report
        return StepResult(
            name=name,
            status="failed",
            duration_sec=round(time.perf_counter() - t0, 3),
            error=str(exc),
        )


def _ablation_per_query_for_significance(ablation_report, top_k: int) -> list[dict]:
    return [
        {
            "method_key": row["variant_key"],
            "method": row["variant"],
            "query_id": row["query_id"],
            "precision_at_k": row["precision_at_k"],
            "recall_at_k": row["recall_at_k"],
            "mrr": row["mrr"],
            "ndcg_at_k": row["ndcg_at_k"],
            "map": row["map"],
            "predicted_ids": row.get("predicted_ids", []),
            "top_k": top_k,
        }
        for row in ablation_report.per_query
    ]


def run_research_pipeline(config: PipelineConfig) -> PipelineResult:
    """Run all nine research stages; artifacts land in config.run_dir."""
    settings = config.settings
    run_dir = config.run_dir
    run_dir.mkdir(parents=True, exist_ok=True)

    steps: list[StepResult] = []
    pipeline_valid = True
    ablation_report = None
    comparison_report = None

    # 1. Dataset validation
    validation = validate_eval_corpus(
        data_dir=config.data_dir,
        eval_path=config.eval_path,
        profiles_path=config.profiles_path,
    )
    val_paths = write_validation_report(validation, run_dir)
    steps.append(
        StepResult(
            name="dataset_validation",
            status="ok" if validation.valid else "failed",
            duration_sec=0.0,
            outputs={k: str(v) for k, v in val_paths.items()},
            error=None if validation.valid else "Corpus validation failed; see dataset_validation.json",
        )
    )
    if not validation.valid:
        pipeline_valid = False
        manifest = _write_manifest(config, steps, pipeline_valid)
        return PipelineResult(
            run_id=run_dir.name,
            run_dir=run_dir,
            manifest_path=manifest,
            steps=steps,
            valid=False,
        )

    # 2. Baseline evaluation (lexical + embedding)
    def run_baseline() -> dict[str, str]:
        nonlocal comparison_report
        bench = ComparisonBenchmark(
            settings=settings,
            eval_path=config.eval_path,
            data_dir=config.data_dir,
            top_k=config.top_k,
        )
        comparison_report = bench.run()
        print_comparison_table(comparison_report)
        paths = write_comparison_report(comparison_report, run_dir, prefix="comparison")
        return {k: str(v) for k, v in paths.items()}

    steps.append(_step("baseline_evaluation", run_baseline))

    # 3. Composite scoring evaluation
    def run_composite() -> dict[str, str]:
        eval_ = CompositeEval(
            settings=settings,
            eval_path=config.eval_path,
            data_dir=config.data_dir,
            top_k=config.top_k,
        )
        report = eval_.run()
        print_composite_summary(report)
        paths = write_composite_report(report, run_dir, prefix="composite")
        return {k: str(v) for k, v in paths.items()}

    steps.append(_step("composite_scoring", run_composite))

    # 4. Ablation study
    def run_ablation() -> dict[str, str]:
        nonlocal ablation_report
        study = AblationStudy(
            settings=settings,
            eval_path=config.eval_path,
            data_dir=config.data_dir,
            top_k=config.top_k,
        )
        ablation_report = study.run()
        print_ablation_summary(ablation_report)
        paths = write_ablation_report(ablation_report, run_dir, prefix="ablation")
        return {k: str(v) for k, v in paths.items()}

    steps.append(_step("ablation_study", run_ablation))

    # 5. Cross-encoder reranking (optional)
    if _cross_encoder_enabled(config):
        def run_ce() -> dict[str, str]:
            report = run_cross_encoder_report(settings=settings, top_k=config.top_k, strategy="composite")
            print_cross_encoder_report(report)
            paths = write_cross_encoder_report(report, run_dir, prefix="cross_encoder")
            return {k: str(v) for k, v in paths.items()}

        steps.append(_step("cross_encoder_reranking", run_ce))
    else:
        steps.append(
            StepResult(
                name="cross_encoder_reranking",
                status="skipped",
                duration_sec=0.0,
                outputs={},
            )
        )

    # 6. Statistical significance
    def run_significance() -> dict[str, str]:
        outputs: dict[str, str] = {}
        if comparison_report is None:
            raise RuntimeError("baseline evaluation did not produce comparison report")

        sig_cmp = run_significance_analysis(
            comparison_report.per_query,
            baseline_key="semantic_cosine",
            n_resamples=config.n_resamples,
            seed=config.seed,
            top_k=config.top_k,
            task="resume_to_jobs",
        )
        sig_cmp.meta["eval_path"] = str(config.eval_path)
        sig_cmp.meta["data_source"] = "comparison"
        print_significance_summary(sig_cmp)
        cmp_paths = write_significance_report(sig_cmp, run_dir, prefix="significance")
        outputs.update({f"comparison_{k}": str(v) for k, v in cmp_paths.items()})

        if ablation_report is not None:
            abl_per_query = _ablation_per_query_for_significance(ablation_report, config.top_k)
            sig_abl = run_significance_analysis(
                abl_per_query,
                baseline_key="semantic_only",
                n_resamples=config.n_resamples,
                seed=config.seed,
                top_k=config.top_k,
                task="resume_to_jobs",
            )
            sig_abl.meta["eval_path"] = str(config.eval_path)
            sig_abl.meta["data_source"] = "ablation"
            print_significance_summary(sig_abl)
            abl_paths = write_significance_report(sig_abl, run_dir, prefix="significance_ablation")
            outputs.update({f"ablation_{k}": str(v) for k, v in abl_paths.items()})

        return outputs

    steps.append(_step("statistical_significance", run_significance))

    # 7. Fairness audit
    def run_fairness() -> dict[str, str]:
        audit = FairnessAudit(
            settings=settings,
            profiles_path=config.profiles_path,
            jobs_path=config.data_dir / "jobs.json",
            top_k=config.top_k,
        )
        report = audit.run()
        print_fairness_audit_summary(report)
        paths = write_fairness_audit_report(report, run_dir, prefix="fairness_audit")
        return {k: str(v) for k, v in paths.items()}

    steps.append(_step("fairness_audit", run_fairness))

    # 8. Explanation evaluation
    def run_explainability() -> dict[str, str]:
        eval_ = ExplainabilityEval(
            settings=settings,
            data_dir=config.data_dir,
            profiles_path=config.profiles_path,
            top_k=config.top_k,
        )
        report = eval_.run()
        print_explainability_summary(report)
        paths = write_explainability_report(report, run_dir, prefix="explainability")
        return {k: str(v) for k, v in paths.items()}

    steps.append(_step("explanation_evaluation", run_explainability))

    # 9. Paper table generation
    def run_paper_tables() -> dict[str, str]:
        paper_dir = run_dir / "paper_tables"
        result = generate_all_paper_tables(
            reports_dir=run_dir,
            out_dir=paper_dir,
            data_dir=config.data_dir,
            top_k=config.top_k,
        )
        return {
            "out_dir": str(result["out_dir"]),
            "manifest": str(paper_dir / "manifest.json"),
            "readme": str(paper_dir / "README.md"),
        }

    steps.append(_step("paper_table_generation", run_paper_tables))

    if any(s.status == "failed" for s in steps):
        pipeline_valid = False

    manifest = _write_manifest(config, steps, pipeline_valid)
    return PipelineResult(
        run_id=run_dir.name,
        run_dir=run_dir,
        manifest_path=manifest,
        steps=steps,
        valid=pipeline_valid,
    )


def _write_manifest(config: PipelineConfig, steps: list[StepResult], valid: bool) -> Path:
    manifest = {
        "run_id": config.run_dir.name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "valid": valid,
        "config": {
            "data_dir": str(config.data_dir),
            "eval_path": str(config.eval_path),
            "profiles_path": str(config.profiles_path),
            "top_k": config.top_k,
            "n_resamples": config.n_resamples,
            "seed": config.seed,
            "cross_encoder_enabled": _cross_encoder_enabled(config),
        },
        "steps": [
            {
                "name": s.name,
                "status": s.status,
                "duration_sec": s.duration_sec,
                "outputs": s.outputs,
                "error": s.error,
            }
            for s in steps
        ],
    }
    path = config.run_dir / "pipeline_manifest.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return path


def make_run_dir(reports_root: Path, run_id: str | None = None) -> Path:
    run_id = run_id or datetime.now(timezone.utc).strftime("research_run_%Y%m%dT%H%M%SZ")
    return reports_root / run_id
