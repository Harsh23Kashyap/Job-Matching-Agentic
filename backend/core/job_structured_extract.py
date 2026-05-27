"""Rule-based structured field extraction from cleaned job description text."""
from __future__ import annotations

import re

from core.resume_structured_extract import _parse_skill_tokens, _unique_strings, split_sections
from core.skill_catalog import canonicalize_skills, normalize_skill_list

KNOWN_JD_SKILLS: frozenset[str] = frozenset(
    {
        "python",
        "java",
        "javascript",
        "typescript",
        "react",
        "node",
        "aws",
        "docker",
        "kubernetes",
        "sql",
        "postgresql",
        "mongodb",
        "fastapi",
        "django",
        "spring boot",
        "flask",
        "go",
        "rust",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "spark",
        "redis",
        "graphql",
        "rest api",
        "azure",
        "google cloud",
        "linux",
        "ci/cd",
        "terraform",
    }
)

INLINE_WITH_SKILLS_RE = re.compile(
    r"\bwith\s+(.+?)\s+and\s+\d+\+?\s*years?",
    re.I,
)

JOB_TITLE_RE = re.compile(
    r"^(?:job\s+title|position|role|opening)\s*:\s*(.+)$",
    re.I,
)
COMPANY_RE = re.compile(
    r"^(?:company|employer|organization)\s*:\s*(.+)$",
    re.I,
)
LOCATION_RE = re.compile(
    r"^(?:location|work\s+location|office)\s*:\s*(.+)$",
    re.I,
)
EXPERIENCE_REQ_RE = re.compile(
    r"(\d+)\+?\s*(?:years?(?:\s+of)?\s+(?:experience|exp\.?)|yrs?(?:\s+of)?\s+experience)",
    re.I,
)

TITLE_FROM_ROLE_RE = re.compile(
    r"^(.{4,80}?)\s+(?:role|position|opening|job)\b",
    re.I,
)
TITLE_BEFORE_AT_RE = re.compile(
    r"^(.{4,80}?)\s+(?:at|@\s)",
    re.I,
)
TITLE_SHORT_LINE_RE = re.compile(
    r"^([A-Z][\w\s/&.-]{2,60}?)(?:[,.]|$)",
)


def _infer_job_title(first_line: str) -> str:
    line = first_line.strip()
    if not line:
        return ""

    role_match = TITLE_FROM_ROLE_RE.match(line)
    if role_match:
        return role_match.group(1).strip()

    at_match = TITLE_BEFORE_AT_RE.match(line)
    if at_match:
        return at_match.group(1).strip()

    if len(line) <= 60 and not re.search(r"[.!?]", line):
        return line

    short_match = TITLE_SHORT_LINE_RE.match(line)
    if short_match and len(short_match.group(1).split()) <= 8:
        return short_match.group(1).strip()

    return ""


def _scan_known_skills(text: str) -> list[str]:
    lowered = text.lower()
    found: list[str] = []
    for skill in sorted(KNOWN_JD_SKILLS, key=len, reverse=True):
        if re.search(rf"\b{re.escape(skill)}\b", lowered):
            found.append(skill)
    return canonicalize_skills(found)


def _skills_from_prose(text: str) -> list[str]:
    collected: list[str] = []
    match = INLINE_WITH_SKILLS_RE.search(text)
    if match:
        collected.extend(_parse_skill_tokens(match.group(1)))
    collected.extend(_scan_known_skills(text))
    return _unique_strings(collected, limit=40)


JD_SECTION_ALIASES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("description", re.compile(r"^(?:about(?:\s+the)?\s+role|job\s+description|overview|responsibilities|what you(?:'|')?ll do)\s*:?\s*$", re.I)),
    ("requirements", re.compile(r"^(?:requirements|qualifications|what we(?:'|')?re looking for|must have|required)\s*:?\s*$", re.I)),
    ("skills", re.compile(r"^(?:required\s+skills|skills|technical\s+skills|tech\s+stack)\s*:?\s*$", re.I)),
    ("education", re.compile(r"^(?:education|academic\s+requirements|degree\s+requirements)\s*:?\s*$", re.I)),
    ("benefits", re.compile(r"^(?:benefits|perks|what we offer)\s*:?\s*$", re.I)),
)


def _split_job_sections(text: str) -> tuple[str, dict[str, str]]:
    preamble, sections = split_sections(text)
    extra: dict[str, list[str]] = {}
    current: str | None = None
    lines = text.split("\n")
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        matched = None
        for key, pattern in JD_SECTION_ALIASES:
            if pattern.match(line):
                matched = key
                break
        if matched:
            current = matched
            extra.setdefault(current, [])
            continue
        if current:
            extra.setdefault(current, []).append(line)
    for key, value in extra.items():
        if key not in sections and value:
            sections[key] = "\n".join(value).strip()
    return preamble, sections


def extract_structured_job(text: str) -> dict:
    preamble, sections = _split_job_sections(text)
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    title = ""
    company = ""
    location = ""
    for line in lines[:20]:
        if not title:
            match = JOB_TITLE_RE.match(line)
            if match:
                title = match.group(1).strip()
                continue
        if not company:
            match = COMPANY_RE.match(line)
            if match:
                company = match.group(1).strip()
                continue
        if not location:
            match = LOCATION_RE.match(line)
            if match:
                location = match.group(1).strip()

    if not title and preamble:
        first = preamble.split("\n", 1)[0].strip()
        if not re.search(r"@|https?://", first):
            title = _infer_job_title(first)

    skills: list[str] = []
    if sections.get("skills"):
        skills.extend(_parse_skill_tokens(sections["skills"]))
    if sections.get("requirements"):
        skills.extend(_parse_skill_tokens(sections["requirements"]))
    for line in lines:
        match = re.match(r"^(?:required\s+skills|skills)\s*:\s*(.+)$", line, re.I)
        if match:
            skills.extend(_parse_skill_tokens(match.group(1)))

    if not skills:
        skills.extend(_skills_from_prose(text))

    required_experience = 0
    for source in (text, sections.get("requirements", ""), sections.get("description", "")):
        match = EXPERIENCE_REQ_RE.search(source)
        if match:
            required_experience = int(match.group(1))
            break

    education_requirements: list[str] = []
    if sections.get("education"):
        for line in sections["education"].split("\n"):
            cleaned = line.strip(" •-*\t")
            if cleaned:
                education_requirements.append(cleaned)

    description_parts = []
    for key in ("description", "requirements", "_preamble"):
        if sections.get(key):
            description_parts.append(sections[key])
    if not description_parts and preamble:
        description_parts.append(preamble)
    description = re.sub(r"\s+", " ", " ".join(description_parts)).strip()[:4000]

    remote_policy = bool(
        re.search(r"\b(remote|work from home|wfh|hybrid|distributed)\b", text, re.I)
    )

    return {
        "title": title,
        "company": company or None,
        "location": location or None,
        "required_skills": _unique_strings(normalize_skill_list(skills), limit=40),
        "required_experience": required_experience,
        "description": description,
        "remote_policy": remote_policy,
        "education_requirements": _unique_strings(education_requirements, limit=6),
        "responsibilities": _unique_strings(
            [line.strip(" •-*\t") for line in (sections.get("description") or "").split("\n") if line.strip()],
            limit=12,
        ),
    }


def merge_job_extraction(rules: dict, llm: dict | None) -> dict:
    merged = dict(rules)
    if not llm:
        return merged

    for key in ("title", "company", "location", "description", "job_type", "link", "budget_currency"):
        llm_value = llm.get(key)
        if llm_value not in (None, ""):
            merged[key] = llm_value
        elif rules.get(key) not in (None, ""):
            merged[key] = rules.get(key)

    llm_skills = llm.get("required_skills") or []
    if isinstance(llm_skills, str):
        llm_skills = [part.strip() for part in llm_skills.split(",") if part.strip()]
    merged["required_skills"] = _unique_strings(
        [*(llm_skills or []), *(rules.get("required_skills") or [])],
        limit=40,
    )

    try:
        llm_exp = int(float(llm.get("required_experience", 0)))
    except (TypeError, ValueError):
        llm_exp = 0
    rules_exp = int(rules.get("required_experience") or 0)
    merged["required_experience"] = llm_exp if llm_exp > 0 else rules_exp

    merged["remote_policy"] = bool(llm.get("remote_policy")) or bool(rules.get("remote_policy"))

    llm_education = llm.get("education_requirements") or []
    if isinstance(llm_education, str):
        llm_education = [llm_education]
    rules_education = rules.get("education_requirements") or []
    merged["education_requirements"] = _unique_strings([*llm_education, *rules_education], limit=8)

    llm_resp = llm.get("responsibilities") or []
    if isinstance(llm_resp, str):
        llm_resp = [llm_resp]
    rules_resp = rules.get("responsibilities") or []
    merged["responsibilities"] = _unique_strings([*llm_resp, *rules_resp], limit=12)

    for budget_key in ("budget_min", "budget_max", "budget"):
        if llm.get(budget_key) is not None:
            merged[budget_key] = llm.get(budget_key)

    return merged
