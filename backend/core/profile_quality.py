"""Rule-based candidate profile quality intelligence."""
from __future__ import annotations

import re
from typing import Any

from core.skill_catalog import canonical_skill, display_for, normalize_skill_list
from core.skill_taxonomy import skill_groups

ACTION_VERB_RE = re.compile(
    r"\b(built|build|designed|design|developed|develop|implemented|implement|led|lead|"
    r"owned|delivered|created|create|optimized|improved|reduced|increased|scaled|deployed|"
    r"managed|collaborated|architected|automated|migrated|launched)\b",
    re.I,
)
METRIC_RE = re.compile(
    r"\b\d+(?:\.\d+)?%|\b\d+\+?\s*(?:users|customers|requests|qps|rps|ms|sec|seconds|minutes|hours|days|"
    r"engineers|people|team members|projects|features|models|pipelines)\b",
    re.I,
)
VAGUE_SUMMARY_RE = re.compile(
    r"\b(hard[\s-]?working|team player|go[\s-]?getter|self[\s-]?motivated|quick learner|"
    r"detail[\s-]?oriented|passionate|enthusiastic|dynamic|results[\s-]?driven)\b",
    re.I,
)
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

INR_EXP_SALARY_BANDS: tuple[tuple[float, float, int, int], ...] = (
    (0, 2, 300_000, 1_500_000),
    (2, 5, 800_000, 3_500_000),
    (5, 10, 1_500_000, 6_000_000),
    (10, 50, 2_500_000, 10_000_000),
)
USD_EXP_SALARY_BANDS: tuple[tuple[float, float, int, int], ...] = (
    (0, 2, 40_000, 120_000),
    (2, 5, 80_000, 180_000),
    (5, 10, 120_000, 250_000),
    (10, 50, 180_000, 400_000),
)

ROLE_SKILL_HINTS: dict[str, list[str]] = {
    "backend": ["Python", "PostgreSQL", "Docker", "REST API"],
    "frontend": ["React", "JavaScript", "TypeScript", "CSS"],
    "full stack": ["React", "Node.js", "PostgreSQL", "REST API"],
    "fullstack": ["React", "Node.js", "PostgreSQL", "REST API"],
    "data": ["Python", "SQL", "Spark", "AWS"],
    "machine learning": ["Python", "Machine Learning", "PyTorch", "SQL"],
    "ml": ["Python", "Machine Learning", "SQL"],
    "devops": ["Docker", "Kubernetes", "AWS", "CI/CD"],
    "android": ["Kotlin", "Android"],
    "ios": ["Swift", "iOS"],
}

_TAXONOMY_SUGGESTIONS: dict[str, list[str]] = {
    "web_backend": ["Docker", "PostgreSQL", "REST API"],
    "web_frontend": ["TypeScript", "CSS"],
    "devops_cloud": ["Linux", "CI/CD", "AWS"],
    "ml_ai": ["Python", "SQL"],
    "data": ["Python", "SQL", "AWS"],
    "programming": ["Git", "SQL"],
}


def quality_payload_from_extracted(extracted: dict) -> dict:
    return {
        "name": extracted.get("name") or "",
        "skills": extracted.get("skills") or [],
        "experience_years": extracted.get("experience_years") or 0,
        "preferred_salary": extracted.get("preferred_salary"),
        "preferred_currency": extracted.get("preferred_currency") or "INR",
        "remote_preference": bool(extracted.get("remote_preference")),
        "summary": extracted.get("summary") or "",
        "email": extracted.get("email") or "",
        "phone": extracted.get("phone") or "",
        "linkedin": extracted.get("linkedin") or "",
        "portfolio": extracted.get("portfolio") or "",
        "other_links": extracted.get("other_links") or [],
    }


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    return []


def _as_float(value: Any) -> float:
    try:
        if value is None or value == "":
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _as_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        amount = int(round(float(value)))
    except (TypeError, ValueError):
        return None
    return amount if amount > 0 else None


def _issue(
    issue_id: str,
    message: str,
    *,
    severity: str = "warning",
    field: str | None = None,
) -> dict[str, str]:
    payload: dict[str, str] = {"id": issue_id, "message": message, "severity": severity}
    if field:
        payload["field"] = field
    return payload


def _salary_band(currency: str, experience: float) -> tuple[int, int] | None:
    bands = USD_EXP_SALARY_BANDS if currency == "USD" else INR_EXP_SALARY_BANDS
    for low, high, min_pay, max_pay in bands:
        if low <= experience < high:
            return min_pay, max_pay
    return None


def _completeness(raw: dict) -> tuple[int, list[dict[str, str]]]:
    score = 0
    missing: list[dict[str, str]] = []

    if str(raw.get("name") or "").strip():
        score += 15
    else:
        missing.append(_issue("missing_name", "Add your full name.", severity="error", field="name"))

    skills = _as_list(raw.get("skills"))
    if skills:
        score += 12
    else:
        missing.append(
            _issue(
                "missing_skills",
                "Add skills — matching relies on them.",
                severity="error",
                field="skills",
            )
        )
    if len(skills) >= 3:
        score += 8
    elif skills:
        missing.append(
            _issue(
                "few_skills",
                "Add at least three skills for sharper job matches.",
                field="skills",
            )
        )

    exp = _as_float(raw.get("experience_years"))
    if exp > 0:
        score += 10
    else:
        missing.append(
            _issue(
                "missing_experience",
                "Set years of experience so level-appropriate jobs surface.",
                field="experience_years",
            )
        )

    if _as_int(raw.get("preferred_salary")):
        score += 10
    elif exp >= 2:
        missing.append(
            _issue(
                "missing_salary",
                "Add expected compensation to reduce pay mismatches.",
                field="preferred_salary",
            )
        )

    summary = str(raw.get("summary") or "").strip()
    if len(summary) >= 80:
        score += 12
    elif summary:
        missing.append(
            _issue(
                "short_summary",
                "Expand your summary to at least 80 characters.",
                field="summary",
            )
        )
    else:
        missing.append(
            _issue(
                "missing_summary",
                "Add a short professional summary.",
                field="summary",
            )
        )

    email = str(raw.get("email") or "").strip()
    phone = str(raw.get("phone") or "").strip()
    if email or phone:
        score += 10
    else:
        missing.append(
            _issue(
                "missing_contact",
                "Add email or phone so employers can reach you.",
                field="email",
            )
        )

    if email and not EMAIL_RE.match(email):
        missing.append(_issue("invalid_email", "Email format looks invalid.", field="email"))

    linkedin = str(raw.get("linkedin") or "").strip()
    portfolio = str(raw.get("portfolio") or "").strip()
    if linkedin or portfolio:
        score += 10
    else:
        missing.append(
            _issue(
                "missing_profile_link",
                "Add LinkedIn or a portfolio link to strengthen credibility.",
                field="linkedin",
            )
        )

    if raw.get("remote_preference") is not None:
        score += 5

    other_links = _as_list(raw.get("other_links"))
    if other_links:
        score += 3

    return min(100, score), missing


def _missing_skills(raw: dict) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    skills = normalize_skill_list(_as_list(raw.get("skills")))
    listed_canon = {canonical_skill(skill) for skill in skills}
    summary = str(raw.get("summary") or "")

    if summary:
        from core.job_structured_extract import _scan_known_skills

        for canon in _scan_known_skills(summary):
            if canon not in listed_canon:
                display = display_for(canon, canon)
                issues.append(
                    _issue(
                        f"skill_in_summary_{canon}",
                        f"“{display}” appears in your summary but is not listed as a skill.",
                        field="skills",
                    )
                )

    if len(skills) < 5 and _as_float(raw.get("experience_years")) >= 3:
        issues.append(
            _issue(
                "sparse_skills_for_seniority",
                "Experienced profiles usually list five or more core skills.",
                field="skills",
            )
        )

    return issues[:6]


def _summary_warnings(raw: dict) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    summary = str(raw.get("summary") or "").strip()
    if not summary:
        return issues

    exp = _as_float(raw.get("experience_years"))
    if len(summary) < 40:
        issues.append(
            _issue(
                "summary_too_short",
                "Summary is very short — add role focus and one accomplishment.",
                field="summary",
            )
        )
    elif exp >= 3 and len(summary) < 120:
        issues.append(
            _issue(
                "summary_thin_for_experience",
                f"With {exp:g}+ years of experience, expand the summary with impact and scope.",
                field="summary",
            )
        )

    if not ACTION_VERB_RE.search(summary):
        issues.append(
            _issue(
                "summary_no_impact_verbs",
                "Use action verbs (built, led, improved) to describe what you delivered.",
                field="summary",
            )
        )

    if VAGUE_SUMMARY_RE.search(summary):
        issues.append(
            _issue(
                "summary_generic_phrases",
                "Swap generic phrases for concrete tools, outcomes, or domains.",
                field="summary",
            )
        )

    if len(summary) >= 80 and not METRIC_RE.search(summary):
        issues.append(
            _issue(
                "summary_no_metrics",
                "Add one measurable outcome (%, latency, users, revenue) if you can.",
                field="summary",
            )
        )

    return issues


def _salary_guidance(raw: dict) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    currency = str(raw.get("preferred_currency") or "INR").upper()
    salary = _as_int(raw.get("preferred_salary"))
    experience = _as_float(raw.get("experience_years"))

    if salary is None:
        if experience >= 1:
            issues.append(
                _issue(
                    "salary_not_set",
                    "Set expected compensation to filter jobs outside your range.",
                    field="preferred_salary",
                )
            )
        return issues

    band = _salary_band(currency, experience)
    if band is None:
        return issues

    band_min, band_max = band
    if salary < band_min * 0.7:
        issues.append(
            _issue(
                "salary_below_market",
                f"Expected pay looks low for {experience:g} years in {currency} — you may match below-market roles only.",
                field="preferred_salary",
            )
        )
    elif salary > band_max * 1.4:
        issues.append(
            _issue(
                "salary_above_market",
                f"Expected pay looks high for {experience:g} years — fewer roles may pass compensation filters.",
                field="preferred_salary",
            )
        )
    else:
        issues.append(
            _issue(
                "salary_in_range",
                f"Compensation looks reasonable for ~{experience:g} years in {currency}.",
                severity="info",
                field="preferred_salary",
            )
        )

    return issues


def _parsing_confidence(
    llm_status: str | None,
    extracted_fields: dict | None,
    raw: dict,
) -> dict[str, Any]:
    if not llm_status:
        return {
            "level": "manual",
            "score": None,
            "message": "Profile edited manually — no resume parse confidence available.",
        }

    base_scores = {"ok": 82, "unavailable": 52, "parse_failed": 28}
    score = base_scores.get(llm_status, 45)

    extracted = extracted_fields or {}
    critical = ("name", "email", "phone", "skills", "summary", "experience_years")
    filled = 0
    for key in critical:
        value = extracted.get(key)
        if key == "skills" and _as_list(value):
            filled += 1
        elif key == "experience_years" and _as_float(value) > 0:
            filled += 1
        elif value not in (None, "", [], 0):
            filled += 1

    score += min(18, filled * 3)

    current_skills = len(normalize_skill_list(_as_list(raw.get("skills"))))
    if current_skills >= 3:
        score += 5

    score = max(0, min(100, score))
    if score >= 75:
        level = "high"
    elif score >= 50:
        level = "medium"
    else:
        level = "low"

    messages = {
        "ok": "LLM-assisted parse succeeded — still verify contact details and skills.",
        "unavailable": "Rule-based parse only — double-check fields against your resume.",
        "parse_failed": "Automatic parse failed — treat extracted fields as unreliable.",
    }
    return {
        "level": level,
        "score": score,
        "message": messages.get(llm_status, "Review parsed fields against your resume."),
        "llm_status": llm_status,
    }


def _skill_suggestions(raw: dict) -> list[str]:
    listed = normalize_skill_list(_as_list(raw.get("skills")))
    listed_canon = {canonical_skill(skill) for skill in listed}
    suggestions: list[str] = []

    combined = " ".join(
        [
            str(raw.get("summary") or ""),
            " ".join(listed),
        ]
    ).lower()
    for hint_key, hint_skills in ROLE_SKILL_HINTS.items():
        if hint_key in combined:
            for skill in hint_skills:
                canon = canonical_skill(skill)
                if canon not in listed_canon:
                    suggestions.append(display_for(canon, skill))

    groups = skill_groups(listed)
    for group in groups:
        for skill in _TAXONOMY_SUGGESTIONS.get(group, []):
            canon = canonical_skill(skill)
            if canon not in listed_canon:
                suggestions.append(display_for(canon, skill))

    deduped: list[str] = []
    seen: set[str] = set()
    for skill in suggestions:
        key = canonical_skill(skill)
        if key in listed_canon or key in seen:
            continue
        seen.add(key)
        deduped.append(skill)
    return deduped[:8]


def _match_suggestions(
    raw: dict,
    missing: list[dict],
    summary_warnings: list[dict],
    salary_guidance: list[dict],
) -> list[dict[str, str]]:
    suggestions: list[dict[str, str]] = []
    skills = _as_list(raw.get("skills"))

    if len(skills) < 3:
        suggestions.append(
            _issue(
                "match_add_skills",
                "Add three or more core skills to improve skill-overlap scoring.",
            )
        )

    if not str(raw.get("summary") or "").strip():
        suggestions.append(
            _issue(
                "match_add_summary",
                "A summary boosts semantic matching beyond skills alone.",
            )
        )

    if _as_int(raw.get("preferred_salary")) is None and _as_float(raw.get("experience_years")) >= 2:
        suggestions.append(
            _issue(
                "match_set_salary",
                "Salary expectations help filter jobs with incompatible pay bands.",
            )
        )

    if not str(raw.get("linkedin") or "").strip():
        suggestions.append(
            _issue(
                "match_add_linkedin",
                "Profiles with LinkedIn often get stronger employer follow-through.",
            )
        )

    if summary_warnings:
        suggestions.append(
            _issue(
                "match_strengthen_summary",
                "A stronger summary improves ranking on semantic similarity.",
            )
        )

    if any(item.get("id") == "skill_in_summary" for item in missing):
        pass

    if not suggestions and not missing:
        suggestions.append(
            _issue(
                "match_ready",
                "Profile looks match-ready — save and run a job search.",
                severity="info",
            )
        )

    return suggestions[:6]


def _quality_score(
    completeness: int,
    missing: list[dict],
    skill_issues: list[dict],
    summary_warnings: list[dict],
    salary_guidance: list[dict],
    parsing: dict[str, Any],
) -> int:
    penalty = 0
    for bucket in (missing, skill_issues, summary_warnings):
        for issue in bucket:
            if issue.get("severity") == "error":
                penalty += 8
            elif issue.get("severity") != "info":
                penalty += 4

    for issue in salary_guidance:
        if issue.get("severity") == "info":
            continue
        penalty += 4

    parse_score = parsing.get("score")
    if isinstance(parse_score, int) and parse_score < 50:
        penalty += 6

    return max(0, min(100, completeness - penalty))


def _grade(score: int) -> str:
    if score >= 80:
        return "strong"
    if score >= 60:
        return "good"
    if score >= 40:
        return "fair"
    return "needs_work"


def _summary_text(score: int, completeness: int, missing: list[dict], parsing: dict) -> str:
    if score >= 80:
        return f"Profile quality {score}/100 — strong for matching."
    hints: list[str] = []
    if any(item.get("field") == "skills" for item in missing):
        hints.append("add skills")
    if any(item.get("field") == "summary" for item in missing):
        hints.append("expand your summary")
    if any(item.get("field") == "preferred_salary" for item in missing):
        hints.append("set salary expectations")
    if parsing.get("level") == "low":
        hints.append("verify parsed fields")
    if hints:
        return f"Profile {completeness}% complete — {', '.join(hints[:3])} to improve matches."
    return f"Profile quality {score}/100 — review suggestions below."


def analyze_profile_quality(
    raw: dict,
    *,
    llm_status: str | None = None,
    extracted_fields: dict | None = None,
) -> dict[str, Any]:
    completeness, missing_fields = _completeness(raw)
    missing_skills = _missing_skills(raw)
    summary_warnings = _summary_warnings(raw)
    salary_guidance = _salary_guidance(raw)
    parsing_confidence = _parsing_confidence(llm_status, extracted_fields, raw)
    skill_suggestions = _skill_suggestions(raw)
    match_suggestions = _match_suggestions(raw, missing_fields, summary_warnings, salary_guidance)
    score = _quality_score(
        completeness,
        missing_fields,
        missing_skills,
        summary_warnings,
        salary_guidance,
        parsing_confidence,
    )

    return {
        "score": score,
        "grade": _grade(score),
        "completeness_percent": completeness,
        "summary": _summary_text(score, completeness, missing_fields, parsing_confidence),
        "missing_fields": missing_fields,
        "missing_skills": missing_skills,
        "summary_warnings": summary_warnings,
        "salary_guidance": salary_guidance,
        "parsing_confidence": parsing_confidence,
        "skill_suggestions": skill_suggestions,
        "match_suggestions": match_suggestions,
    }
