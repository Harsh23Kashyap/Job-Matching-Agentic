from core.skill_catalog import canonicalize_skills


def _format_skills(skills: list[str], canonical: bool) -> str:
    items = canonicalize_skills(skills) if canonical else sorted({s.strip().lower() for s in skills})
    return ", ".join(items)


def resume_document_text(cv: dict, canonical_skills: bool = True) -> str:
    work_mode = "remote" if cv.get("remote_preference") else "onsite"
    lines = [
        "resume profile",
        f"name: {cv.get('name', '')}",
        f"email: {cv.get('email', '')}",
        f"phone: {cv.get('phone', '')}",
        f"linkedin: {cv.get('linkedin', '')}",
        f"portfolio: {cv.get('portfolio', '')}",
        f"experience_years: {cv.get('experience_years', 0)}",
        f"work_mode: {work_mode}",
        f"skills: {_format_skills(cv.get('skills', []), canonical_skills)}",
        f"summary: {cv.get('summary', '')}",
    ]
    other_links = cv.get("other_links") or []
    if other_links:
        lines.append(f"other_links: {', '.join(other_links)}")
    return "\n".join(lines)


def job_document_text(job: dict, canonical_skills: bool = True) -> str:
    work_mode = "remote" if job.get("remote_policy") else "onsite"
    lines = [
        "job description",
        f"title: {job.get('title', '')}",
        f"company: {job.get('company', '')}",
        f"location: {job.get('location', '')}",
        f"job_type: {job.get('job_type', '')}",
        f"required_experience_years: {job.get('required_experience', 0)}",
        f"work_mode: {work_mode}",
        f"required_skills: {_format_skills(job.get('required_skills', []), canonical_skills)}",
        f"description: {job.get('description', '')}",
        f"apply_link: {job.get('link', '')}",
    ]
    return "\n".join(lines)
