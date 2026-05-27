"""Automated checks for match explanation quality (offline research only)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable

from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.skill_catalog import normalize
from core.skills import skill_overlap_details

SKILL_LIST_PATTERNS = [
    re.compile(r"matching skills:\s*(.+)", re.IGNORECASE),
    re.compile(r"matched skills:\s*(.+)", re.IGNORECASE),
    re.compile(r"gaps:\s*(.+)", re.IGNORECASE),
    re.compile(r"missing[^:]*:\s*(.+)", re.IGNORECASE),
]

COMPONENT_CLAIM_CHECKS: list[tuple[re.Pattern[str], Callable[[ScoreBreakdown], bool], str]] = [
    (
        re.compile(r"high semantic similarity", re.IGNORECASE),
        lambda b: b.semantic_score >= 0.65,
        "high_semantic_claim",
    ),
    (
        re.compile(r"moderate semantic similarity", re.IGNORECASE),
        lambda b: 0.5 <= b.semantic_score < 0.65,
        "moderate_semantic_claim",
    ),
    (
        re.compile(r"experience aligns", re.IGNORECASE),
        lambda b: b.experience_score is not None and b.experience_score >= 0.8,
        "experience_claim",
    ),
    (
        re.compile(r"compensation expectations align", re.IGNORECASE),
        lambda b: b.compensation_score is not None and b.compensation_score >= 0.85,
        "compensation_claim",
    ),
    (
        re.compile(r"remote/work setup aligns", re.IGNORECASE),
        lambda b: b.location_score is not None and b.location_score >= 0.9,
        "location_claim",
    ),
    (
        re.compile(r"multimodal blend", re.IGNORECASE),
        lambda b: b.strategy_used == "multimodal",
        "multimodal_claim",
    ),
    (
        re.compile(r"composite score blends", re.IGNORECASE),
        lambda b: b.strategy_used == "composite",
        "composite_claim",
    ),
]

GENERIC_ONLY_PATTERNS = [
    re.compile(r"^high semantic similarity\.?$", re.IGNORECASE),
    re.compile(r"^moderate semantic similarity\.?$", re.IGNORECASE),
    re.compile(r"^composite score blends", re.IGNORECASE),
]


@dataclass
class ExplanationAudit:
    candidate_id: str
    job_id: str
    explain_mode: str
    bullets: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    mentioned_skills: list[str] = field(default_factory=list)
    hallucinated_skills: list[str] = field(default_factory=list)
    checks: dict[str, bool] = field(default_factory=dict)
    component_alignment: dict[str, bool] = field(default_factory=dict)
    violations: list[str] = field(default_factory=list)
    specificity_score: float = 0.0
    faithfulness_score: float = 0.0
    flagged: bool = False


def _allowed_skill_norms(candidate: CandidateSnapshot, job: JobSnapshot) -> set[str]:
    allowed: set[str] = set()
    for skill in candidate.skills:
        allowed.add(normalize(skill))
    for skill in job.required_skills + job.preferred_skills:
        allowed.add(normalize(skill))
    return allowed


def parse_skill_lists_from_bullets(bullets: list[str]) -> list[str]:
    found: list[str] = []
    for bullet in bullets:
        for pattern in SKILL_LIST_PATTERNS:
            match = pattern.search(bullet)
            if match:
                chunk = match.group(1).split(".")[0]
                for part in chunk.split(","):
                    token = part.strip()
                    if token:
                        found.append(token)
    return found


def extract_mentioned_skills(
    bullets: list[str],
    *,
    vocabulary: list[str],
    allowed_norms: set[str],
) -> tuple[list[str], list[str]]:
    """Return (mentioned_allowed, hallucinated) skill strings found in bullets."""
    text = " ".join(bullets).lower()
    parsed = parse_skill_lists_from_bullets(bullets)

    mentioned: list[str] = []
    hallucinated: list[str] = []

    for token in parsed:
        norm = normalize(token)
        if norm in allowed_norms:
            mentioned.append(token)
        else:
            hallucinated.append(token)

    for skill in vocabulary:
        norm = normalize(skill)
        if len(norm) < 2:
            continue
        if norm in text and skill not in mentioned and normalize(skill) not in {normalize(m) for m in mentioned}:
            if norm in allowed_norms:
                mentioned.append(skill)
            else:
                hallucinated.append(skill)

    # dedupe preserving order
    def dedupe(items: list[str]) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []
        for item in items:
            key = normalize(item)
            if key not in seen:
                seen.add(key)
                out.append(item)
        return out

    return dedupe(mentioned), dedupe(hallucinated)


def mentions_matched_or_missing(
    bullets: list[str],
    matched: list[str],
    missing: list[str],
) -> bool:
    text = " ".join(bullets).lower()
    for skill in matched + missing:
        if normalize(skill) in text:
            return True
    parsed = parse_skill_lists_from_bullets(bullets)
    if parsed:
        return True
    for pattern in ("matching skills", "matched skills", "gaps:", "missing skill"):
        if pattern in text:
            return True
    return False


def check_component_alignment(bullets: list[str], breakdown: ScoreBreakdown) -> dict[str, bool]:
    text = " ".join(bullets)
    alignment: dict[str, bool] = {}
    for pattern, predicate, key in COMPONENT_CLAIM_CHECKS:
        if pattern.search(text):
            alignment[key] = predicate(breakdown)
    return alignment


def compute_specificity(bullets: list[str], matched: list[str], missing: list[str]) -> float:
    """0–1 score: concrete skill references vs generic-only bullets."""
    if not bullets:
        return 0.0
    text = " ".join(bullets).lower()
    has_skill = any(normalize(s) in text for s in matched + missing)
    has_parsed = bool(parse_skill_lists_from_bullets(bullets))
    generic_only = all(any(p.match(b.strip()) for p in GENERIC_ONLY_PATTERNS) for b in bullets)
    if has_skill or has_parsed:
        return 1.0 if len(bullets) >= 2 else 0.75
    if generic_only:
        return 0.25
    if any("overlap" in b.lower() or "similarity" in b.lower() for b in bullets):
        return 0.5
    return 0.4


def audit_explanation(
    *,
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    breakdown: ScoreBreakdown,
    bullets: list[str],
    explain_mode: str,
    vocabulary: list[str],
) -> ExplanationAudit:
    matched, missing = skill_overlap_details(candidate.skills, job.required_skills)
    allowed = _allowed_skill_norms(candidate, job)
    mentioned, hallucinated = extract_mentioned_skills(
        bullets, vocabulary=vocabulary, allowed_norms=allowed
    )
    component_alignment = check_component_alignment(bullets, breakdown)

    checks = {
        "mentions_matched_or_missing_skill": mentions_matched_or_missing(bullets, matched, missing),
        "no_hallucinated_skills": len(hallucinated) == 0,
        "component_claims_valid": all(component_alignment.values()) if component_alignment else True,
        "has_specific_skill_reference": bool(mentioned) or any(
            normalize(s) in " ".join(bullets).lower() for s in matched + missing
        ),
        "non_empty": len(bullets) > 0,
    }

    violations: list[str] = []
    if not checks["mentions_matched_or_missing_skill"]:
        violations.append("missing_skill_reference")
    if not checks["no_hallucinated_skills"]:
        violations.append("hallucinated_skills")
    if not checks["component_claims_valid"]:
        failed = [k for k, ok in component_alignment.items() if not ok]
        violations.append(f"component_mismatch:{','.join(failed)}")
    if checks["non_empty"] and not checks["has_specific_skill_reference"] and (matched or missing):
        violations.append("too_generic")

    specificity = compute_specificity(bullets, matched, missing)
    hard_checks = [
        checks["mentions_matched_or_missing_skill"],
        checks["no_hallucinated_skills"],
        checks["component_claims_valid"],
    ]
    faithfulness = sum(1 for ok in hard_checks if ok) / len(hard_checks)

    flagged = bool(violations)

    return ExplanationAudit(
        candidate_id=candidate.id,
        job_id=job.id,
        explain_mode=explain_mode,
        bullets=bullets,
        matched_skills=matched,
        missing_skills=missing,
        mentioned_skills=mentioned,
        hallucinated_skills=hallucinated,
        checks=checks,
        component_alignment=component_alignment,
        violations=violations,
        specificity_score=round(specificity, 4),
        faithfulness_score=round(faithfulness, 4),
        flagged=flagged,
    )


def consistency_between_profiles(
    audit_a: ExplanationAudit,
    audit_b: ExplanationAudit,
    *,
    min_jaccard: float = 0.5,
) -> dict[str, Any]:
    set_a = set(audit_a.bullets)
    set_b = set(audit_b.bullets)
    union = set_a | set_b
    jaccard = len(set_a & set_b) / len(union) if union else 1.0
    matched_a = set(normalize(s) for s in audit_a.matched_skills)
    matched_b = set(normalize(s) for s in audit_b.matched_skills)
    same_matched = matched_a == matched_b
    return {
        "jaccard_similarity": round(jaccard, 4),
        "drift_score": round(1.0 - jaccard, 4),
        "same_matched_skills": same_matched,
        "consistent": jaccard >= min_jaccard and same_matched,
        "bullets_a": audit_a.bullets,
        "bullets_b": audit_b.bullets,
    }
