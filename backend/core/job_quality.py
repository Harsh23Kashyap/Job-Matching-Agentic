"""Rule-based job posting quality intelligence for employers."""
from __future__ import annotations

import re
from typing import Any

from core.skill_catalog import canonical_skill, display_for, normalize_skill_list
from core.skill_taxonomy import skill_groups

SENIOR_TITLE_RE = re.compile(
    r"\b(senior|sr\.?|lead|principal|staff|architect|head of|director|manager)\b",
    re.I,
)
JUNIOR_TITLE_RE = re.compile(
    r"\b(junior|jr\.?|intern|trainee|associate|entry[\s-]?level|graduate|fresher)\b",
    re.I,
)
ACTION_VERB_RE = re.compile(
    r"\b(build|design|develop|implement|maintain|own|lead|drive|deliver|create|optimize|scale|deploy|manage|collaborate|write|test|architect)\b",
    re.I,
)
YEARS_IN_TEXT_RE = re.compile(
    r"\d+\+?\s*(?:years?(?:\s+of)?\s+(?:experience|exp\.?)|yrs?(?:\s+of)?\s+experience)",
    re.I,
)
VAGUE_PHRASES: tuple[tuple[str, str], ...] = (
    (r"\betc\.?\b", "Avoid vague catch-alls like “etc.”, list concrete requirements."),
    (r"\band more\b", "Replace “and more” with specific skills or responsibilities."),
    (r"\bgood communication\b", "Specify communication expectations (stakeholders, docs, presentations)."),
    (r"\bteam player\b", "Describe collaboration context instead of generic “team player”."),
    (r"\bfast[\s-]?paced\b", "Clarify pace with concrete delivery expectations."),
    (r"\bself[\s-]?starter\b", "State ownership scope instead of “self-starter”."),
    (r"\bas needed\b", "Replace “as needed” with defined responsibilities."),
    (r"\bother duties\b", "List primary duties explicitly rather than “other duties”."),
)

TITLE_SKILL_HINTS: dict[str, list[str]] = {
    "backend": ["Python", "PostgreSQL", "Docker", "REST API"],
    "frontend": ["React", "JavaScript", "TypeScript", "CSS"],
    "full stack": ["React", "Node.js", "PostgreSQL", "REST API"],
    "fullstack": ["React", "Node.js", "PostgreSQL", "REST API"],
    "data engineer": ["Python", "SQL", "Spark", "AWS"],
    "data scientist": ["Python", "Machine Learning", "SQL", "pandas"],
    "machine learning": ["Python", "Machine Learning", "PyTorch", "SQL"],
    "devops": ["Docker", "Kubernetes", "AWS", "CI/CD"],
    "sre": ["Linux", "Kubernetes", "AWS", "CI/CD"],
    "mobile": ["Kotlin", "Swift", "React Native", "REST API"],
    "android": ["Kotlin", "Android", "REST API"],
    "ios": ["Swift", "iOS", "REST API"],
    "product manager": ["SQL", "Figma", "REST API"],
}

# Typical annual max (INR) bands by experience tier for warning heuristics.
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

_TAXONOMY_SUGGESTIONS: dict[str, list[str]] = {
    "web_backend": ["Docker", "PostgreSQL", "REST API", "CI/CD"],
    "web_frontend": ["TypeScript", "CSS", "REST API"],
    "devops_cloud": ["Linux", "Terraform", "Docker", "CI/CD"],
    "ml_ai": ["Python", "SQL", "pandas"],
    "data": ["Python", "SQL", "AWS"],
    "programming": ["Git", "SQL"],
    "mobile": ["REST API", "CI/CD"],
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


def _missing_fields(raw: dict) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if not str(raw.get("title") or "").strip():
        issues.append(_issue("missing_title", "Add a job title.", severity="error", field="title"))
    if not str(raw.get("company") or "").strip():
        issues.append(_issue("missing_company", "Add a company name so candidates know who is hiring.", field="company"))
    if not str(raw.get("location") or "").strip() and not raw.get("remote_policy"):
        issues.append(
            _issue(
                "missing_location",
                "Add a location or mark the role as remote-friendly.",
                field="location",
            )
        )
    skills = _as_list(raw.get("required_skills"))
    if not skills:
        issues.append(
            _issue(
                "missing_skills",
                "Add required skills, matching depends on them.",
                severity="error",
                field="required_skills",
            )
        )
    elif len(skills) < 3:
        issues.append(
            _issue(
                "few_skills",
                "Add at least three required skills for sharper candidate matches.",
                field="required_skills",
            )
        )
    description = str(raw.get("description") or "").strip()
    if len(description) < 80:
        issues.append(
            _issue(
                "missing_description",
                "Write a fuller description (80+ characters) covering responsibilities and expectations.",
                field="description",
            )
        )
    if not str(raw.get("job_type") or "").strip():
        issues.append(_issue("missing_job_type", "Specify employment type (full-time, contract, etc.).", field="job_type"))
    budget_min = _as_int(raw.get("budget_min"))
    budget_max = _as_int(raw.get("budget_max"))
    budget = _as_int(raw.get("budget"))
    if budget_min is None and budget_max is None and budget is None:
        issues.append(
            _issue(
                "missing_budget",
                "Add a salary or budget range to reduce mismatched applicants.",
                field="budget_min",
            )
        )
    exp = _as_float(raw.get("required_experience"))
    if exp <= 0 and not JUNIOR_TITLE_RE.search(str(raw.get("title") or "")):
        issues.append(
            _issue(
                "missing_experience",
                "Set required years of experience unless this is an entry-level role.",
                field="required_experience",
            )
        )
    return issues


def _unclear_requirements(raw: dict) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    title = str(raw.get("title") or "")
    description = str(raw.get("description") or "")
    combined = f"{title}\n{description}".strip()
    lowered = combined.lower()

    if description and len(description) >= 80 and not ACTION_VERB_RE.search(description):
        issues.append(
            _issue(
                "no_action_verbs",
                "Description reads vague, add action verbs (build, design, own, deliver).",
                field="description",
            )
        )

    for pattern, message in VAGUE_PHRASES:
        if re.search(pattern, lowered, re.I):
            issues.append(_issue("vague_language", message, field="description"))
            break

    if raw.get("remote_policy") and re.search(r"\bon[\s-]?site\b|\bin[\s-]?office\b", lowered):
        issues.append(
            _issue(
                "remote_conflict",
                "Remote-friendly is checked but the description mentions on-site work, clarify hybrid vs remote.",
                field="remote_policy",
            )
        )

    if len(_as_list(raw.get("required_skills"))) == 1 and len(description) > 200:
        issues.append(
            _issue(
                "skills_too_narrow",
                "Only one required skill listed for a detailed role, split stack skills explicitly.",
                field="required_skills",
            )
        )

    if title and len(title.split()) <= 2 and len(description) < 120:
        issues.append(
            _issue(
                "thin_posting",
                "Title and description are both thin, expand what success looks like in the role.",
                field="description",
            )
        )

    return issues


def _salary_warnings(raw: dict) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    currency = str(raw.get("budget_currency") or "INR").upper()
    budget_min = _as_int(raw.get("budget_min"))
    budget_max = _as_int(raw.get("budget_max"))
    budget = _as_int(raw.get("budget"))
    experience = _as_float(raw.get("required_experience"))

    if budget_min is not None and budget_max is None and budget is None:
        issues.append(
            _issue(
                "budget_max_missing",
                "Add a maximum budget so candidates know the top of the range.",
                field="budget_max",
            )
        )
    if budget_min is not None and budget_max is not None and budget_min > budget_max:
        issues.append(
            _issue(
                "budget_inverted",
                "Minimum budget is higher than maximum, swap or fix the range.",
                severity="error",
                field="budget_max",
            )
        )

    effective_max = budget_max or budget or budget_min
    band = _salary_band(currency, experience)
    if effective_max is not None and band is not None:
        _, band_max = band
        band_min, _ = band
        if effective_max < band_min:
            issues.append(
                _issue(
                    "budget_low_for_experience",
                    f"Budget looks low for {experience:g}+ years in {currency}, may attract underqualified or uninterested candidates.",
                    field="budget_max",
                )
            )
        elif effective_max > band_max * 1.8:
            issues.append(
                _issue(
                    "budget_high_for_experience",
                    f"Budget looks high relative to {experience:g} years required, confirm the range is intentional.",
                    field="budget_max",
                )
            )

    if budget_min is not None and budget_max is not None:
        spread = budget_max - budget_min
        if spread > 0 and spread / max(budget_max, 1) > 0.6:
            issues.append(
                _issue(
                    "budget_wide_range",
                    "Budget range is very wide, a tighter band sets clearer expectations.",
                    field="budget_max",
                )
            )

    return issues


def _skill_suggestions(raw: dict) -> list[str]:
    listed = normalize_skill_list(_as_list(raw.get("required_skills")))
    listed_canon = {canonical_skill(skill) for skill in listed}
    suggestions: list[str] = []

    title_lower = str(raw.get("title") or "").lower()
    for hint_key, hint_skills in TITLE_SKILL_HINTS.items():
        if hint_key in title_lower:
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

    description = str(raw.get("description") or "")
    if description:
        from core.job_structured_extract import _scan_known_skills

        for canon in _scan_known_skills(description):
            if canon not in listed_canon:
                suggestions.append(display_for(canon, canon))

    deduped: list[str] = []
    seen: set[str] = set()
    for skill in suggestions:
        key = canonical_skill(skill)
        if key in listed_canon or key in seen:
            continue
        seen.add(key)
        deduped.append(skill)
    return deduped[:8]


def _experience_warnings(raw: dict) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    title = str(raw.get("title") or "")
    description = str(raw.get("description") or "")
    experience = _as_float(raw.get("required_experience"))

    if SENIOR_TITLE_RE.search(title) and experience < 5:
        issues.append(
            _issue(
                "senior_title_low_years",
                f"Title suggests a senior role but required experience is {experience:g} years, align title and years.",
                field="required_experience",
            )
        )
    if JUNIOR_TITLE_RE.search(title) and experience > 4:
        issues.append(
            _issue(
                "junior_title_high_years",
                f"Title suggests entry-level but {experience:g} years are required, clarify level.",
                field="required_experience",
            )
        )
    if experience >= 8 and not SENIOR_TITLE_RE.search(title):
        issues.append(
            _issue(
                "high_years_plain_title",
                f"{experience:g}+ years required but the title does not signal seniority, candidates may skip or misread the level.",
                field="title",
            )
        )
    if experience > 0 and description and not YEARS_IN_TEXT_RE.search(description):
        issues.append(
            _issue(
                "experience_not_in_description",
                "Required experience is set but not mentioned in the description, add it for clarity.",
                field="description",
            )
        )
    if experience <= 0 and not JUNIOR_TITLE_RE.search(title) and SENIOR_TITLE_RE.search(title):
        issues.append(
            _issue(
                "senior_title_no_years",
                "Senior title with 0 required years, set experience or adjust the title.",
                field="required_experience",
            )
        )
    return issues


def _quality_score(
    raw: dict,
    missing: list[dict],
    unclear: list[dict],
    salary: list[dict],
    experience: list[dict],
) -> int:
    score = 0
    if str(raw.get("title") or "").strip():
        score += 12
    if str(raw.get("company") or "").strip():
        score += 8
    if str(raw.get("location") or "").strip() or raw.get("remote_policy"):
        score += 8
    skills = _as_list(raw.get("required_skills"))
    if skills:
        score += 10
    if len(skills) >= 3:
        score += 8
    description = str(raw.get("description") or "").strip()
    if len(description) >= 80:
        score += 10
    if len(description) >= 200:
        score += 5
    if str(raw.get("job_type") or "").strip():
        score += 5
    exp = _as_float(raw.get("required_experience"))
    if exp > 0 or JUNIOR_TITLE_RE.search(str(raw.get("title") or "")):
        score += 8
    budget_min = _as_int(raw.get("budget_min"))
    budget_max = _as_int(raw.get("budget_max"))
    budget = _as_int(raw.get("budget"))
    if budget_min or budget_max or budget:
        score += 10
    if budget_min and budget_max:
        score += 5
    if raw.get("remote_policy") is not None:
        score += 3

    penalty = 0
    for bucket in (missing, unclear, salary, experience):
        for issue in bucket:
            if issue.get("severity") == "error":
                penalty += 8
            else:
                penalty += 4
    return max(0, min(100, score - penalty))


def _grade(score: int) -> str:
    if score >= 80:
        return "strong"
    if score >= 60:
        return "good"
    if score >= 40:
        return "fair"
    return "needs_work"


def _summary(score: int, missing: list[dict], unclear: list[dict], salary: list[dict], experience: list[dict]) -> str:
    if score >= 80 and not (missing or unclear or salary or experience):
        return "Posting looks strong, candidates should understand the role and match well."
    hints: list[str] = []
    if any(item.get("field") == "required_skills" for item in missing):
        hints.append("add required skills")
    if any(item.get("id") == "missing_budget" for item in missing):
        hints.append("add a budget range")
    if any(item.get("field") == "description" for item in missing + unclear):
        hints.append("expand the description")
    if salary:
        hints.append("review compensation")
    if experience:
        hints.append("align title and experience")
    if hints:
        return f"Job quality score {score}/100, {', '.join(hints[:3])} to improve matches."
    return f"Job quality score {score}/100, review the suggestions below."


def analyze_job_quality(raw: dict) -> dict[str, Any]:
    missing_fields = _missing_fields(raw)
    unclear_requirements = _unclear_requirements(raw)
    salary_warnings = _salary_warnings(raw)
    experience_warnings = _experience_warnings(raw)
    skill_suggestions = _skill_suggestions(raw)
    score = _quality_score(raw, missing_fields, unclear_requirements, salary_warnings, experience_warnings)

    return {
        "score": score,
        "grade": _grade(score),
        "summary": _summary(score, missing_fields, unclear_requirements, salary_warnings, experience_warnings),
        "missing_fields": missing_fields,
        "unclear_requirements": unclear_requirements,
        "salary_warnings": salary_warnings,
        "skill_suggestions": skill_suggestions,
        "experience_warnings": experience_warnings,
    }
