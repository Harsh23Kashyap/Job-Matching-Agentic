from core.embedding import embed_skill
from core.similarity import cosine_similarity
from core.skill_catalog import canonical_skill, canonicalize_skills, normalize_skills


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


# Frozen graded-credit weights (EXP-034; fixed a priori, NOT tuned on any evaluation):
# exact canonical match = full credit; same ESCO-lite taxonomy group = partial; otherwise none.
GRADED_EXACT_CREDIT = 1.0
GRADED_RELATED_CREDIT = 0.5


def graded_coverage_skills(
    resume_skills: list[str],
    job_skills: list[str],
    related_credit: float = GRADED_RELATED_CREDIT,
) -> float:
    """Relation-aware required-coverage: for each job skill, take the best graded credit from any
    resume skill (exact=1.0, same-taxonomy-group=related_credit, else 0.0), averaged over the job skills.

    Unlike binary Jaccard this gives PARTIAL credit for related-but-not-identical skills and is
    coverage-oriented (how well the candidate covers the job's requirements), while never awarding
    exact-level credit to a merely-related skill. The default related_credit=0.5 is frozen a priori
    (see PROTOCOL.md); the parameter exists only for the reported robustness sweep."""
    from core.skill_taxonomy import skill_groups

    if not job_skills:
        return 0.0
    resume_canon = {canonical_skill(s) for s in resume_skills if canonical_skill(s)}
    resume_groups = skill_groups(resume_skills)
    total = 0.0
    for job_skill in job_skills:
        jc = canonical_skill(job_skill)
        if not jc:
            continue
        if jc in resume_canon:
            total += GRADED_EXACT_CREDIT
            continue
        jg = skill_groups([job_skill])
        if jg and resume_groups and (jg & resume_groups):
            total += related_credit
    return total / len(job_skills)


def skills_score(
    resume_skills: list[str],
    job_skills: list[str],
    skills_mode: str,
    model_name: str,
) -> float:
    if skills_mode == "embedding":
        return soft_overlap(resume_skills, job_skills, model_name=model_name)
    if skills_mode == "graded":
        return graded_coverage_skills(resume_skills, job_skills)
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
