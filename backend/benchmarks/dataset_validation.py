"""Validate offline evaluation corpus before running research benchmarks."""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED_CV_FIELDS = {"id", "skills", "experience_years"}
REQUIRED_JOB_FIELDS = {"id", "required_skills", "required_experience"}


@dataclass
class ValidationIssue:
    level: str  # error | warning
    code: str
    message: str


@dataclass
class ValidationReport:
    valid: bool
    meta: dict[str, Any]
    stats: dict[str, Any]
    issues: list[ValidationIssue] = field(default_factory=list)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_eval_corpus(
    *,
    data_dir: Path,
    eval_path: Path | None = None,
    profiles_path: Path | None = None,
) -> ValidationReport:
    """Check cvs, jobs, eval labels, and optional fairness profiles."""
    eval_path = eval_path or data_dir / "eval_pairs.json"
    profiles_path = profiles_path or data_dir / "fairness_audit_profiles.json"
    issues: list[ValidationIssue] = []

    cvs_path = data_dir / "cvs.json"
    jobs_path = data_dir / "jobs.json"

    for path, label in ((cvs_path, "cvs.json"), (jobs_path, "jobs.json"), (eval_path, "eval_pairs.json")):
        if not path.is_file():
            issues.append(ValidationIssue("error", "missing_file", f"Missing {label}: {path}"))

    if any(i.code == "missing_file" for i in issues):
        return ValidationReport(
            valid=False,
            meta={"generated_at": datetime.now(timezone.utc).isoformat(), "data_dir": str(data_dir)},
            stats={},
            issues=issues,
        )

    resumes = _load_json(cvs_path)
    jobs = _load_json(jobs_path)
    eval_payload = _load_json(eval_path)

    if not isinstance(resumes, list):
        issues.append(ValidationIssue("error", "invalid_cvs", "cvs.json must be a JSON array"))
    if not isinstance(jobs, list):
        issues.append(ValidationIssue("error", "invalid_jobs", "jobs.json must be a JSON array"))

    cv_ids: set[str] = set()
    if isinstance(resumes, list):
        for idx, cv in enumerate(resumes):
            if not isinstance(cv, dict):
                issues.append(ValidationIssue("error", "invalid_cv_row", f"CV row {idx} is not an object"))
                continue
            missing = REQUIRED_CV_FIELDS - set(cv)
            if missing:
                issues.append(
                    ValidationIssue("error", "cv_missing_fields", f"CV row {idx} missing fields: {sorted(missing)}")
                )
            cid = cv.get("id")
            if not cid:
                issues.append(ValidationIssue("error", "cv_missing_id", f"CV row {idx} has no id"))
            elif cid in cv_ids:
                issues.append(ValidationIssue("error", "duplicate_cv_id", f"Duplicate CV id: {cid}"))
            else:
                cv_ids.add(str(cid))

    job_ids: set[str] = set()
    if isinstance(jobs, list):
        for idx, job in enumerate(jobs):
            if not isinstance(job, dict):
                issues.append(ValidationIssue("error", "invalid_job_row", f"Job row {idx} is not an object"))
                continue
            missing = REQUIRED_JOB_FIELDS - set(job)
            if missing:
                issues.append(
                    ValidationIssue("error", "job_missing_fields", f"Job row {idx} missing fields: {sorted(missing)}")
                )
            jid = job.get("id")
            if not jid:
                issues.append(ValidationIssue("error", "job_missing_id", f"Job row {idx} has no id"))
            elif jid in job_ids:
                issues.append(ValidationIssue("error", "duplicate_job_id", f"Duplicate job id: {jid}"))
            else:
                job_ids.add(str(jid))

    labels = eval_payload.get("labels", eval_payload if isinstance(eval_payload, list) else [])
    if not isinstance(labels, list):
        issues.append(ValidationIssue("error", "invalid_labels", "eval_pairs labels must be a list"))
        labels = []

    relevance_scale = str(eval_payload.get("relevance_scale", "0-2"))
    max_rel = 3 if "3" in relevance_scale else 2

    query_ids: set[str] = set()
    rel_counter: Counter[int] = Counter()
    unknown_queries: set[str] = set()
    unknown_docs: set[str] = set()

    for idx, item in enumerate(labels):
        if not isinstance(item, dict):
            issues.append(ValidationIssue("error", "invalid_label_row", f"Label row {idx} is not an object"))
            continue
        qid = item.get("query_id")
        doc_id = item.get("doc_id")
        if qid is None or doc_id is None:
            issues.append(ValidationIssue("error", "label_missing_ids", f"Label row {idx} missing query_id or doc_id"))
            continue
        qid, doc_id = str(qid), str(doc_id)
        query_ids.add(qid)
        if qid not in cv_ids:
            unknown_queries.add(qid)
        if doc_id not in job_ids:
            unknown_docs.add(doc_id)
        try:
            rel = int(item["relevance"])
        except (KeyError, TypeError, ValueError):
            issues.append(ValidationIssue("error", "invalid_relevance", f"Label row {idx} has invalid relevance"))
            continue
        if rel < 0:
            continue
        if rel > max_rel:
            issues.append(
                ValidationIssue("warning", "relevance_out_of_scale", f"Label row {idx} relevance {rel} > {max_rel}")
            )
        rel_counter[rel] += 1

    for qid in sorted(unknown_queries):
        issues.append(ValidationIssue("error", "unknown_query_id", f"query_id not in cvs.json: {qid}"))
    for doc_id in sorted(unknown_docs):
        issues.append(ValidationIssue("error", "unknown_doc_id", f"doc_id not in jobs.json: {doc_id}"))

    unlabeled_cvs = cv_ids - query_ids
    if unlabeled_cvs:
        issues.append(
            ValidationIssue(
                "warning",
                "unlabeled_candidates",
                f"{len(unlabeled_cvs)} candidates have no labeled pairs in eval_pairs.json",
            )
        )

    fairness_pairs = 0
    if profiles_path.is_file():
        profiles_payload = _load_json(profiles_path)
        pairs = profiles_payload.get("pairs", profiles_payload if isinstance(profiles_payload, list) else [])
        if isinstance(pairs, list):
            fairness_pairs = len(pairs)
        else:
            issues.append(ValidationIssue("warning", "invalid_fairness_profiles", "fairness_audit_profiles.json malformed"))
    else:
        issues.append(
            ValidationIssue("warning", "missing_fairness_profiles", f"Optional fairness profiles missing: {profiles_path}")
        )

    stats = {
        "candidates": len(cv_ids),
        "jobs": len(job_ids),
        "labeled_pairs": sum(rel_counter.values()),
        "labeled_queries": len(query_ids),
        "relevance_distribution": dict(sorted(rel_counter.items())),
        "relevance_scale": relevance_scale,
        "fairness_profile_pairs": fairness_pairs,
    }

    if stats["candidates"] == 0:
        issues.append(ValidationIssue("error", "empty_corpus", "cvs.json contains no candidates"))
    if stats["jobs"] == 0:
        issues.append(ValidationIssue("error", "empty_corpus", "jobs.json contains no jobs"))
    if stats["labeled_pairs"] == 0:
        issues.append(ValidationIssue("error", "no_labels", "eval_pairs.json has no graded relevance labels"))
    if stats["labeled_queries"] == 0:
        issues.append(ValidationIssue("error", "no_queries", "eval_pairs.json has no labeled query_ids"))

    valid = not any(i.level == "error" for i in issues)
    meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "data_dir": str(data_dir),
        "eval_path": str(eval_path),
        "profiles_path": str(profiles_path),
        "task": eval_payload.get("task", "resume_to_jobs"),
    }
    return ValidationReport(valid=valid, meta=meta, stats=stats, issues=issues)


def write_validation_report(report: ValidationReport, out_dir: Path) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "json": out_dir / "dataset_validation.json",
        "markdown": out_dir / "dataset_validation.md",
    }
    payload = {
        "valid": report.valid,
        "meta": report.meta,
        "stats": report.stats,
        "issues": [{"level": i.level, "code": i.code, "message": i.message} for i in report.issues],
    }
    paths["json"].write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Dataset Validation",
        "",
        f"**Status:** {'PASS' if report.valid else 'FAIL'}",
        "",
        "## Corpus stats",
        "",
        f"- Candidates: {report.stats.get('candidates', 0)}",
        f"- Jobs: {report.stats.get('jobs', 0)}",
        f"- Labeled queries: {report.stats.get('labeled_queries', 0)}",
        f"- Labeled pairs: {report.stats.get('labeled_pairs', 0)}",
        f"- Relevance scale: {report.stats.get('relevance_scale', 'n/a')}",
        f"- Relevance distribution: {report.stats.get('relevance_distribution', {})}",
        f"- Fairness profile pairs: {report.stats.get('fairness_profile_pairs', 0)}",
        "",
    ]
    if report.issues:
        lines.extend(["## Issues", ""])
        for issue in report.issues:
            lines.append(f"- [{issue.level.upper()}] `{issue.code}`: {issue.message}")
        lines.append("")

    paths["markdown"].write_text("\n".join(lines), encoding="utf-8")
    return paths
