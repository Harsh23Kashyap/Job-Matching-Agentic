"""Synthetic controlled profiles for offline fairness audit; no real-user inference."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from contracts.snapshots import CandidateSnapshot
from core.document_text import resume_document_text
from core.embedding import embed_text

MATCH_RELEVANT_FIELDS = (
    "skills",
    "experience_years",
    "remote_preference",
    "preferred_salary",
    "summary",
)

DEMOGRAPHIC_FIELDS = (
    "name",
    "email",
    "phone",
    "linkedin",
    "summary_suffix",
    "nationality_label",
    "hometown_label",
    "pronouns_label",
)


def load_audit_profiles(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not payload.get("meta", {}).get("synthetic"):
        raise ValueError("Fairness audit profiles must be marked synthetic in meta.synthetic")
    return payload


def merge_variant_cv(core: dict[str, Any], variant: dict[str, Any], *, pair_id: str) -> dict[str, Any]:
    """Build one synthetic CV dict from shared core + demographic variant fields."""
    suffix = variant["suffix"]
    summary = core["summary"]
    if variant.get("summary_suffix"):
        summary = f"{summary} {variant['summary_suffix']}"
    if variant.get("nationality_label"):
        summary = f"{summary} {variant['nationality_label']}"
    if variant.get("hometown_label"):
        summary = f"{summary} {variant['hometown_label']}"
    if variant.get("pronouns_label"):
        summary = f"{summary} {variant['pronouns_label']}"

    cv = {
        "id": f"{pair_id}_{suffix}",
        "name": variant.get("name", f"Candidate {suffix.upper()}"),
        "skills": list(core["skills"]),
        "experience_years": core["experience_years"],
        "remote_preference": core["remote_preference"],
        "preferred_salary": core.get("preferred_salary"),
        "summary": summary,
        "email": variant.get("email", f"{pair_id}.{suffix}@example.test"),
        "phone": variant.get("phone", "+1-555-0100"),
    }
    if variant.get("linkedin"):
        cv["linkedin"] = variant["linkedin"]
    return cv


def validate_pair(pair: dict[str, Any]) -> None:
    core = pair["core"]
    for field in MATCH_RELEVANT_FIELDS:
        if field not in core:
            raise ValueError(f"Pair {pair['pair_id']} missing core field: {field}")
    if len(pair.get("variants", [])) != 2:
        raise ValueError(f"Pair {pair['pair_id']} must have exactly two variants")


def audit_cv_to_snapshot(cv: dict[str, Any], model_name: str) -> CandidateSnapshot:
    doc = resume_document_text(cv)
    doc_hash = hashlib.sha256(doc.encode("utf-8")).hexdigest()
    emb = embed_text(doc, model_name=model_name).tolist()
    return CandidateSnapshot(
        id=cv["id"],
        name=cv.get("name", ""),
        skills=list(cv.get("skills", [])),
        experience_years=float(cv.get("experience_years", 0)),
        remote_preference=bool(cv.get("remote_preference", False)),
        preferred_salary=cv.get("preferred_salary"),
        summary=str(cv.get("summary", "")),
        version=1,
        document_text_hash=doc_hash,
        embedding=emb,
    )


def build_pair_snapshots(
    pair: dict[str, Any],
    model_name: str,
) -> tuple[dict[str, Any], CandidateSnapshot, CandidateSnapshot]:
    validate_pair(pair)
    core = pair["core"]
    v_a, v_b = pair["variants"]
    cv_a = merge_variant_cv(core, v_a, pair_id=pair["pair_id"])
    cv_b = merge_variant_cv(core, v_b, pair_id=pair["pair_id"])
    return pair, audit_cv_to_snapshot(cv_a, model_name), audit_cv_to_snapshot(cv_b, model_name)
