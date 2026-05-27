"""Rule-based resume improvement suggestions for a target job."""
from __future__ import annotations

import re
from typing import Any

from contracts.profiles import CandidateProfile, JobProfile

_STOPWORDS = frozenset(
    {
        "and",
        "the",
        "for",
        "with",
        "you",
        "your",
        "our",
        "will",
        "this",
        "that",
        "from",
        "have",
        "has",
        "are",
        "was",
        "were",
        "role",
        "job",
        "work",
        "team",
        "using",
        "used",
        "into",
        "about",
        "years",
        "year",
        "experience",
        "looking",
        "strong",
        "skills",
        "required",
        "preferred",
        "ability",
        "including",
        "such",
        "must",
        "should",
        "can",
        "all",
        "any",
        "who",
        "what",
        "when",
        "where",
        "how",
        "not",
        "but",
        "also",
        "etc",
        "via",
        "per",
        "new",
        "one",
        "two",
        "three",
    }
)

_BULLET_RE = re.compile(r"^[-•*]\s+|^\d+[.)]\s+")


def _skill_set(skills: list[str]) -> set[str]:
    return {s.strip().lower() for s in skills if s and s.strip()}


def _candidate_text(profile: CandidateProfile) -> str:
    parts = [
        profile.summary,
        profile.document_text,
        " ".join(profile.skills),
        profile.name,
    ]
    return " ".join(p for p in parts if p).lower()


def _job_text(job: JobProfile) -> str:
    parts = [
        job.title,
        job.description,
        job.company or "",
        job.location or "",
        " ".join(job.required_skills),
        " ".join(job.preferred_skills),
    ]
    return " ".join(p for p in parts if p)


def _tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{1,}", text.lower())
    return [t for t in tokens if len(t) >= 3 and t not in _STOPWORDS]


def missing_skills_for_job(candidate: CandidateProfile, job: JobProfile) -> list[str]:
    owned = _skill_set(candidate.skills)
    return [skill for skill in job.required_skills if skill.lower() not in owned]


def weak_skills_for_job(candidate: CandidateProfile, job: JobProfile) -> list[str]:
    corpus = _candidate_text(candidate)
    weak: list[str] = []
    job_skills = _skill_set(job.required_skills + job.preferred_skills)
    for skill in candidate.skills:
        key = skill.lower()
        if key not in job_skills:
            continue
        if key not in corpus or corpus.count(key) < 2:
            weak.append(skill)
    return weak


def missing_keywords_for_job(candidate: CandidateProfile, job: JobProfile) -> list[str]:
    resume_tokens = set(_tokenize(_candidate_text(candidate)))
    resume_tokens.update(_skill_set(candidate.skills))
    keywords: list[str] = []
    seen: set[str] = set()

    for skill in job.required_skills + job.preferred_skills:
        key = skill.lower()
        if key not in resume_tokens and key not in seen:
            keywords.append(skill)
            seen.add(key)

    for token in _tokenize(_job_text(job)):
        if token in resume_tokens or token in seen:
            continue
        if any(token in skill.lower() for skill in candidate.skills):
            continue
        keywords.append(token.title() if token.isalpha() else token)
        seen.add(token)
        if len(keywords) >= 12:
            break
    return keywords


def _extract_bullets(profile: CandidateProfile) -> list[str]:
    bullets: list[str] = []
    if profile.document_text:
        for line in profile.document_text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if _BULLET_RE.match(stripped):
                bullets.append(_BULLET_RE.sub("", stripped).strip())
            elif len(stripped) > 35 and not stripped.endswith(":"):
                bullets.append(stripped)
    if not bullets and profile.summary:
        bullets.append(profile.summary.strip())
    return bullets[:5]


def _suggest_summary(candidate: CandidateProfile, job: JobProfile, missing: list[str], weak: list[str]) -> str:
    matched = [s for s in candidate.skills if s.lower() in _skill_set(job.required_skills)]
    focus = matched[:3] or candidate.skills[:3]
    gaps = missing[:3] or weak[:2]
    focus_text = ", ".join(focus) if focus else "your core strengths"
    if gaps:
        gap_text = ", ".join(gaps)
        return (
            f"{candidate.experience_years:g}-year professional targeting the {job.title} role. "
            f"Lead with {focus_text}, and add credible examples of {gap_text} where you have real experience."
        )
    return (
        f"{candidate.experience_years:g}-year professional with strengths in {focus_text}, "
        f"positioned for the {job.title} role at {job.company or 'this company'}."
    )


def _suggest_bullets(
    profile: CandidateProfile,
    job: JobProfile,
    missing: list[str],
    keywords: list[str],
) -> list[dict[str, str]]:
    originals = _extract_bullets(profile)
    if not originals:
        originals = [profile.summary or f"Experience relevant to {job.title}"]

    focus_terms = (missing + keywords)[:4]
    improvements: list[dict[str, str]] = []
    for original in originals:
        term = next((t for t in focus_terms if t.lower() not in original.lower()), None)
        if term:
            suggested = f"{original.rstrip('.')}, using {term} where accurate."
            reason = f"Mention {term} so ATS and recruiters see alignment with the {job.title} posting."
        else:
            suggested = f"{original.rstrip('.')} — quantify impact (metrics, scale, or outcomes)."
            reason = "Add measurable outcomes recruiters can scan quickly."
        improvements.append({"original": original, "suggested": suggested, "reason": reason})
        if len(improvements) >= 4:
            break
    return improvements


def _ats_checklist(candidate: CandidateProfile, job: JobProfile) -> list[dict[str, str]]:
    text = _candidate_text(candidate)
    required = job.required_skills
    matched_required = [s for s in required if s.lower() in _skill_set(candidate.skills) or s.lower() in text]
    coverage = len(matched_required) / max(len(required), 1)

    checks: list[dict[str, str]] = []

    def add(item: str, ok: bool, pass_tip: str, fail_tip: str) -> None:
        checks.append(
            {
                "item": item,
                "status": "pass" if ok else ("warn" if item.startswith("Optional") else "fail"),
                "tip": pass_tip if ok else fail_tip,
            }
        )

    add(
        "Contact details present",
        bool(candidate.email or candidate.phone),
        "Email or phone is visible for recruiter follow-up.",
        "Add a work email or phone number to your profile.",
    )
    add(
        "Professional summary",
        len(candidate.summary.strip()) >= 40,
        "Summary gives recruiters a quick positioning statement.",
        "Add a 2–3 sentence summary tailored to your target roles.",
    )
    add(
        "Skills list populated",
        len(candidate.skills) >= 3,
        "Skills help keyword matching and quick scanning.",
        "List at least three core skills from the job posting you genuinely have.",
    )
    add(
        "Required skill coverage",
        coverage >= 0.6,
        f"Covers {len(matched_required)}/{len(required)} required skills from the posting.",
        f"Only {len(matched_required)}/{len(required)} required skills appear — add missing skills you truly have.",
    )
    add(
        "Quantified achievements",
        bool(re.search(r"\d", candidate.summary + candidate.document_text)),
        "Numbers help demonstrate impact.",
        "Add metrics (%, users, latency, revenue, team size) to at least one bullet.",
    )
    add(
        "Optional: LinkedIn or portfolio link",
        bool(candidate.linkedin or candidate.portfolio),
        "Extra links give recruiters more context.",
        "Add LinkedIn or a portfolio link if you have one.",
    )
    return checks


def build_rule_based_suggestions(candidate: CandidateProfile, job: JobProfile) -> dict[str, Any]:
    missing = missing_skills_for_job(candidate, job)
    weak = weak_skills_for_job(candidate, job)
    keywords = missing_keywords_for_job(candidate, job)
    return {
        "job_id": job.id,
        "job_title": job.title,
        "missing_keywords": keywords,
        "weak_skills": weak,
        "missing_skills": missing,
        "suggested_summary": _suggest_summary(candidate, job, missing, weak),
        "bullet_improvements": _suggest_bullets(candidate, job, missing, keywords),
        "ats_checklist": _ats_checklist(candidate, job),
    }


def merge_llm_suggestions(base: dict[str, Any], llm_payload: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key in ("missing_keywords", "weak_skills", "missing_skills"):
        values = llm_payload.get(key)
        if isinstance(values, list) and values:
            seen: set[str] = set()
            combined: list[str] = []
            for item in list(base.get(key, [])) + [str(v) for v in values]:
                token = item.strip()
                if not token:
                    continue
                lower = token.lower()
                if lower in seen:
                    continue
                seen.add(lower)
                combined.append(token)
            merged[key] = combined[:12] if key == "missing_keywords" else combined[:10]

    summary = llm_payload.get("suggested_summary")
    if isinstance(summary, str) and summary.strip():
        merged["suggested_summary"] = summary.strip()

    bullets = llm_payload.get("bullet_improvements")
    if isinstance(bullets, list) and bullets:
        cleaned: list[dict[str, str]] = []
        for row in bullets[:5]:
            if not isinstance(row, dict):
                continue
            original = str(row.get("original") or "").strip()
            suggested = str(row.get("suggested") or "").strip()
            reason = str(row.get("reason") or "").strip()
            if original and suggested:
                cleaned.append({"original": original, "suggested": suggested, "reason": reason or "Improve alignment with the role."})
        if cleaned:
            merged["bullet_improvements"] = cleaned

    checklist = llm_payload.get("ats_checklist")
    if isinstance(checklist, list) and checklist:
        cleaned_checks: list[dict[str, str]] = []
        for row in checklist:
            if not isinstance(row, dict):
                continue
            item = str(row.get("item") or "").strip()
            status = str(row.get("status") or "warn").strip().lower()
            tip = str(row.get("tip") or "").strip()
            if item and status in {"pass", "warn", "fail"}:
                cleaned_checks.append({"item": item, "status": status, "tip": tip or "Review this item."})
        if cleaned_checks:
            merged["ats_checklist"] = cleaned_checks

    return merged


def build_resume_suggestions(
    candidate: CandidateProfile,
    job: JobProfile,
    llm: Any | None = None,
) -> dict[str, Any]:
    base = build_rule_based_suggestions(candidate, job)
    base["llm_status"] = "rule_based"
    base["disclaimer"] = (
        "Suggestions only — your saved profile is not changed. Copy ideas into your profile or resume editor manually."
    )

    if llm is None:
        return base

    from hooks.llm_parser import LlmUnavailableError, LlmParseError

    candidate_ctx = {
        "name": candidate.name,
        "skills": candidate.skills,
        "experience_years": candidate.experience_years,
        "summary": candidate.summary,
        "document_text": (candidate.document_text or "")[:6000],
        "email": candidate.email,
        "phone": candidate.phone,
        "linkedin": candidate.linkedin,
        "portfolio": candidate.portfolio,
    }
    job_ctx = {
        "title": job.title,
        "company": job.company,
        "required_skills": job.required_skills,
        "preferred_skills": job.preferred_skills,
        "required_experience": job.required_experience,
        "description": job.description,
        "location": job.location,
        "remote_policy": job.remote_policy,
        "job_type": job.job_type,
    }

    try:
        llm_payload = llm.suggest_resume_for_job(candidate_ctx, job_ctx)
        merged = merge_llm_suggestions(base, llm_payload)
        merged["llm_status"] = "ok"
        merged["disclaimer"] = base["disclaimer"]
        return merged
    except LlmUnavailableError:
        base["message"] = "AI coach unavailable — showing rule-based suggestions."
        return base
    except LlmParseError:
        base["message"] = "Could not generate AI suggestions — showing rule-based suggestions."
        return base
