from core.embedding import embed_skill
from core.similarity import cosine_similarity
from core.skill_catalog import canonicalize_skills, normalize_skills


def jaccard_skills(resume_skills: list[str], job_skills: list[str]) -> float:
    a = set(canonicalize_skills(resume_skills))
    b = set(canonicalize_skills(job_skills))
    if not a and not b:
        return 0.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def soft_overlap(resume_skills: list[str], job_skills: list[str], model_name: str) -> float:
    if not resume_skills or not job_skills:
        return 0.0
    resume_vecs = [embed_skill(s, model_name=model_name) for s in resume_skills]
    bests: list[float] = []
    for job_skill in job_skills:
        j_vec = embed_skill(job_skill, model_name=model_name)
        best = max(cosine_similarity(j_vec, r_vec) for r_vec in resume_vecs)
        bests.append(best)
    return sum(bests) / len(bests)


def hierarchical_skills_score(
    resume_skills: list[str],
    required_skills: list[str],
    preferred_skills: list[str],
    *,
    skills_mode: str,
    model_name: str,
    must_weight: float = 0.7,
) -> float:
    """Must-have vs preferred skill coverage with configurable blend."""
    must = skills_score(resume_skills, required_skills, skills_mode, model_name)
    if not preferred_skills:
        return must
    pref = skills_score(resume_skills, preferred_skills, skills_mode, model_name)
    return must_weight * must + (1.0 - must_weight) * pref


def taxonomy_skills_score(resume_skills: list[str], job_skills: list[str]) -> float:
    from core.skill_taxonomy import taxonomy_overlap

    return taxonomy_overlap(resume_skills, job_skills)


def skills_score(
    resume_skills: list[str],
    job_skills: list[str],
    skills_mode: str,
    model_name: str,
) -> float:
    if skills_mode == "embedding":
        return soft_overlap(resume_skills, job_skills, model_name=model_name)
    return jaccard_skills(resume_skills, job_skills)


def raw_skill_overlap(resume_skills: list[str], job_skills: list[str]) -> list[str]:
    r = set(canonicalize_skills(resume_skills))
    j = set(canonicalize_skills(job_skills))
    return sorted(r & j)


def skill_overlap_details(resume_skills: list[str], job_skills: list[str]) -> tuple[list[str], list[str]]:
    resume_entries = {entry.canonical: entry for entry in normalize_skills(resume_skills)}
    job_entries = {entry.canonical: entry for entry in normalize_skills(job_skills)}
    overlap = set(resume_entries) & set(job_entries)
    matched = sorted({job_entries[key].display for key in overlap}, key=str.lower)
    missing = sorted(
        {job_entries[key].display for key in job_entries if key not in overlap},
        key=str.lower,
    )
    return matched, missing
