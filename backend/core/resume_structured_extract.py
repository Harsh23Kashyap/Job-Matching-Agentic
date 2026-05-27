"""Rule-based structured field extraction from cleaned resume text."""
from __future__ import annotations

import re
from datetime import datetime

from core.contact_extract import extract_contact_from_text, merge_contact_fields
from core.skill_catalog import canonicalize_skills, normalize_skill_list

SECTION_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("summary", re.compile(r"^(?:professional\s+)?(?:summary|profile|objective|about(?:\s+me)?)\s*:?\s*$", re.I)),
    ("skills", re.compile(r"^(?:technical\s+)?(?:skills|core\s+competencies|technologies|tools)\s*:?\s*$", re.I)),
    ("experience", re.compile(r"^(?:work\s+)?(?:experience|employment|professional\s+experience|work\s+history)\s*:?\s*$", re.I)),
    ("education", re.compile(r"^(?:education|academic\s+background|qualifications)\s*:?\s*$", re.I)),
    ("projects", re.compile(r"^(?:personal\s+)?(?:projects|key\s+projects|selected\s+projects)\s*:?\s*$", re.I)),
)

INLINE_SECTION_RE = re.compile(
    r"^(skills|technical skills|experience|education|projects|summary|objective)\s*:\s*(.+)$",
    re.I,
)

YEARS_EXPERIENCE_RE = re.compile(
    r"(\d+(?:\.\d+)?)\+?\s*(?:years?(?:\s+of)?\s+(?:experience|exp\.?)|yrs?(?:\s+of)?\s+(?:experience|exp\.?))",
    re.I,
)

DATE_RANGE_RE = re.compile(
    r"(?:"
    r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?"
    r"|\d{1,2}"
    r")"
    r"[\s./-]*"
    r"(?:\d{2,4}|present|current|now)"
    r"\s*[-–—to]+\s*"
    r"(?:"
    r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?"
    r"|\d{1,2}"
    r")"
    r"[\s./-]*"
    r"(?:\d{2,4}|present|current|now)",
    re.I,
)

DEGREE_HINT_RE = re.compile(
    r"\b("
    r"b\.?\s*tech|b\.?\s*e\.?|bachelor|m\.?\s*tech|m\.?\s*e\.?|master|mba|ph\.?\s*d|"
    r"b\.?\s*sc|m\.?\s*sc|b\.?\s*com|m\.?\s*com|diploma|associate"
    r")\b",
    re.I,
)

REMOTE_HINT_RE = re.compile(r"\b(remote|work from home|wfh|hybrid|distributed)\b", re.I)

SALARY_RE = re.compile(
    r"(?:expected|desired|target)?\s*(?:salary|ctc|compensation)\s*[:|-]?\s*"
    r"(?:₹|rs\.?|inr|\$|usd|€|eur|£|gbp|sgd)?\s*"
    r"(\d[\d,]*(?:\.\d+)?)\s*(?:lpa|lac|lakh|k|m)?",
    re.I,
)

BULLET_PREFIX_RE = re.compile(r"^[\s•·▪●○◦‣⁃\-\*\u2022]+")


def _strip_bullet(line: str) -> str:
    return BULLET_PREFIX_RE.sub("", line).strip()


def _unique_strings(values: list[str], *, limit: int = 32) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        cleaned = re.sub(r"\s+", " ", value).strip(" ,;|-")
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(cleaned)
        if len(out) >= limit:
            break
    return out


def split_sections(text: str) -> tuple[str, dict[str, str]]:
    preamble: list[str] = []
    sections: dict[str, list[str]] = {}
    current: str | None = None

    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            if current:
                sections.setdefault(current, []).append("")
            elif preamble:
                preamble.append("")
            continue

        inline = INLINE_SECTION_RE.match(line)
        if inline:
            section_key = inline.group(1).lower().replace(" ", "_")
            if section_key == "objective":
                section_key = "summary"
            if section_key == "technical_skills":
                section_key = "skills"
            if current:
                sections.setdefault(current, [])
            current = section_key
            sections.setdefault(current, []).append(inline.group(2).strip())
            continue

        matched_header: str | None = None
        for key, pattern in SECTION_PATTERNS:
            if pattern.match(line):
                matched_header = key
                break
        if matched_header:
            current = matched_header
            sections.setdefault(current, [])
            continue

        if current:
            sections.setdefault(current, []).append(line)
        else:
            preamble.append(line)

    normalized = {key: "\n".join(lines).strip() for key, lines in sections.items() if any(line.strip() for line in lines)}
    return "\n".join(preamble).strip(), normalized


def _parse_skill_tokens(text: str) -> list[str]:
    if not text:
        return []
    chunks = re.split(r"[\n,;|/•·▪]+", text)
    tokens: list[str] = []
    for chunk in chunks:
        item = _strip_bullet(chunk.strip())
        if not item:
            continue
        if ":" in item and len(item.split(":", 1)[0]) <= 16:
            _, rhs = item.split(":", 1)
            item = rhs.strip()
        tokens.extend(part.strip() for part in re.split(r"\s{2,}|\t", item) if part.strip())
    return normalize_skill_list([token for token in tokens if 1 < len(token) <= 48])


def extract_skills(text: str, sections: dict[str, str]) -> list[str]:
    collected: list[str] = []
    if sections.get("skills"):
        collected.extend(_parse_skill_tokens(sections["skills"]))
    for line in text.split("\n"):
        match = re.match(r"^(?:technical\s+)?skills\s*:\s*(.+)$", line.strip(), re.I)
        if match:
            collected.extend(_parse_skill_tokens(match.group(1)))
    if sections.get("projects"):
        collected.extend(_parse_skill_tokens(sections["projects"]))
    if sections.get("experience"):
        for token in _parse_skill_tokens(sections["experience"]):
            if token in {
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
                "spring",
                "go",
                "rust",
                "c++",
                "machine learning",
            }:
                collected.append(token)
    return _unique_strings(collected, limit=40)


def _years_from_date_ranges(text: str) -> float:
    total_months = 0
    now = datetime.now()
    for match in DATE_RANGE_RE.finditer(text):
        span = match.group(0)
        if re.search(r"present|current|now", span, re.I):
            left = span.split("-")[0].strip()
            year_match = re.search(r"(20\d{2}|19\d{2})", left)
            if year_match:
                years = now.year - int(year_match.group(1))
                total_months += max(0, years * 12)
    if total_months:
        return min(50.0, round(total_months / 12, 1))
    return 0.0


def extract_experience_years(text: str, sections: dict[str, str]) -> float:
    sources = [sections.get("experience", ""), sections.get("summary", ""), text[:3000]]
    for source in sources:
        match = YEARS_EXPERIENCE_RE.search(source)
        if match:
            return min(50.0, float(match.group(1)))
    exp_section = sections.get("experience", "")
    if exp_section:
        ranged = _years_from_date_ranges(exp_section)
        if ranged:
            return ranged
    return 0.0


def _entries_from_section(section: str, *, limit: int = 8) -> list[str]:
    if not section:
        return []
    entries: list[str] = []
    buffer: list[str] = []
    for raw_line in section.split("\n"):
        line = _strip_bullet(raw_line.strip())
        if not line:
            if buffer:
                entries.append(" ".join(buffer))
                buffer = []
            continue
        if buffer and (line[0].isupper() or DEGREE_HINT_RE.search(line) or re.match(r"^\d{4}", line)):
            entries.append(" ".join(buffer))
            buffer = [line]
        else:
            buffer.append(line)
    if buffer:
        entries.append(" ".join(buffer))
    return _unique_strings(entries, limit=limit)


def extract_education(sections: dict[str, str]) -> list[dict[str, str]]:
    section = sections.get("education", "")
    entries = _entries_from_section(section)
    results: list[dict[str, str]] = []
    for entry in entries:
        degree_match = DEGREE_HINT_RE.search(entry)
        year_match = re.search(r"(19|20)\d{2}", entry)
        results.append(
            {
                "text": entry,
                "degree": degree_match.group(0) if degree_match else "",
                "year": year_match.group(0) if year_match else "",
            }
        )
    return results[:6]


def extract_projects(sections: dict[str, str]) -> list[dict[str, str]]:
    section = sections.get("projects", "")
    entries = _entries_from_section(section)
    results: list[dict[str, str]] = []
    for entry in entries:
        tech = _parse_skill_tokens(entry)
        title = entry.split("—")[0].split(" - ")[0].strip()
        if len(title) > 96:
            title = title[:96].rstrip() + "…"
        results.append(
            {
                "name": title,
                "description": entry,
                "technologies": tech[:8],
            }
        )
    return results[:8]


def extract_summary(preamble: str, sections: dict[str, str]) -> str:
    if sections.get("summary"):
        return re.sub(r"\s+", " ", sections["summary"]).strip()[:1200]
    lines = [line.strip() for line in preamble.split("\n") if line.strip()]
    body: list[str] = []
    for line in lines[1:]:
        if re.search(r"@|https?://|linkedin\.com|github\.com|\+\d", line, re.I):
            continue
        if SECTION_PATTERNS and any(pattern.match(line) for _, pattern in SECTION_PATTERNS):
            break
        body.append(line)
        if len(body) >= 4:
            break
    summary = " ".join(body).strip()
    return summary[:1200]


def detect_remote_preference(text: str) -> bool:
    return bool(REMOTE_HINT_RE.search(text))


def extract_preferred_salary(text: str) -> int | None:
    match = SALARY_RE.search(text)
    if not match:
        return None
    raw = match.group(1).replace(",", "")
    try:
        value = float(raw)
    except ValueError:
        return None
    tail = text[match.end() : match.end() + 8].lower()
    if "lpa" in tail or "lac" in tail or "lakh" in tail:
        value *= 100000
    elif raw.endswith("k") or " k" in tail:
        value *= 1000
    elif raw.endswith("m") or " m" in tail:
        value *= 1_000_000
    return int(value)


def extract_structured_resume(text: str) -> dict:
    preamble, sections = split_sections(text)
    contact = extract_contact_from_text(text)
    skills = extract_skills(text, sections)
    experience_years = extract_experience_years(text, sections)
    education = extract_education(sections)
    projects = extract_projects(sections)
    summary = extract_summary(preamble, sections)

    return {
        **contact,
        "skills": skills,
        "experience_years": experience_years,
        "preferred_salary": extract_preferred_salary(text),
        "remote_preference": detect_remote_preference(text),
        "summary": summary,
        "education": education,
        "projects": projects,
    }


def merge_resume_extraction(rules: dict, llm: dict | None) -> dict:
    """Merge rule-based extraction with optional LLM output (LLM preferred, rules fill gaps)."""
    merged = dict(rules)
    if not llm:
        return merged

    contact = merge_contact_fields(llm, rules)
    for key in ("name", "email", "phone", "linkedin", "portfolio", "other_links"):
        merged[key] = contact.get(key) or rules.get(key) or ("" if key != "other_links" else [])

    llm_skills = llm.get("skills") or []
    if isinstance(llm_skills, str):
        llm_skills = [part.strip() for part in llm_skills.split(",") if part.strip()]
    merged["skills"] = _unique_strings([*(llm_skills or []), *(rules.get("skills") or [])], limit=40)

    llm_exp = llm.get("experience_years")
    try:
        llm_exp = float(llm_exp)
    except (TypeError, ValueError):
        llm_exp = 0.0
    rules_exp = float(rules.get("experience_years") or 0)
    merged["experience_years"] = llm_exp if llm_exp > 0 else rules_exp

    llm_summary = str(llm.get("summary") or "").strip()
    rules_summary = str(rules.get("summary") or "").strip()
    merged["summary"] = llm_summary if len(llm_summary) >= 20 else (rules_summary or llm_summary)

    if llm.get("preferred_salary") is not None:
        merged["preferred_salary"] = llm.get("preferred_salary")
    elif rules.get("preferred_salary") is not None:
        merged["preferred_salary"] = rules.get("preferred_salary")

    merged["remote_preference"] = bool(llm.get("remote_preference")) or bool(rules.get("remote_preference"))

    llm_education = llm.get("education") or []
    merged["education"] = llm_education if llm_education else rules.get("education") or []

    llm_projects = llm.get("projects") or []
    merged["projects"] = llm_projects if llm_projects else rules.get("projects") or []

    if llm.get("preferred_currency"):
        merged["preferred_currency"] = llm.get("preferred_currency")

    return merged
