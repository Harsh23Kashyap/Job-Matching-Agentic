"""Find similar jobs or candidates using embedding + skill overlap."""
from __future__ import annotations

from typing import Any

import numpy as np

from agents.candidate_agent import CandidateAgent
from agents.employer_agent import EmployerAgent
from contracts.profiles import CandidateProfile, JobProfile
from core.similarity import cosine_similarity
from core.skills import jaccard_skills, skill_overlap_details

EMBEDDING_WEIGHT = 0.6
SKILLS_WEIGHT = 0.4


def _combined_score(embedding_score: float, skills_score: float) -> float:
    return EMBEDDING_WEIGHT * embedding_score + SKILLS_WEIGHT * skills_score


def _job_skill_pool(job: JobProfile) -> list[str]:
    return list(job.required_skills) + list(job.preferred_skills)


def _public_job_item(job: JobProfile, scores: dict[str, float], matched_skills: list[str]) -> dict[str, Any]:
    return {
        "id": job.id,
        "label": job.title,
        "subtitle": job.company or job.location or "",
        "similarity_score": round(scores["combined"], 4),
        "embedding_score": round(scores["embedding"], 4),
        "skills_score": round(scores["skills"], 4),
        "matched_skills": matched_skills[:5],
        "remote_policy": job.remote_policy,
    }


def _public_candidate_item(
    profile: CandidateProfile,
    scores: dict[str, float],
    matched_skills: list[str],
) -> dict[str, Any]:
    years = profile.experience_years
    subtitle = f"{years:g} yr experience" if years else ""
    return {
        "id": profile.id,
        "label": profile.name,
        "subtitle": subtitle,
        "similarity_score": round(scores["combined"], 4),
        "embedding_score": round(scores["embedding"], 4),
        "skills_score": round(scores["skills"], 4),
        "matched_skills": matched_skills[:5],
        "experience_years": profile.experience_years,
    }


def find_similar_jobs(
    employer_agent: EmployerAgent,
    job_id: str,
    *,
    limit: int = 3,
) -> list[dict[str, Any]]:
    anchor = employer_agent.get_by_id(job_id)
    if anchor is None or not anchor.embedding:
        return []

    anchor_vec = np.asarray(anchor.embedding, dtype=np.float32)
    anchor_skills = _job_skill_pool(anchor)
    ranked: list[tuple[float, dict[str, Any]]] = []

    for job in employer_agent.list_jobs():
        if job.id == job_id or not job.embedding:
            continue
        if job.status == "closed":
            continue
        peer_skills = _job_skill_pool(job)
        emb = cosine_similarity(anchor_vec, np.asarray(job.embedding, dtype=np.float32))
        skills = jaccard_skills(anchor_skills, peer_skills)
        combined = _combined_score(emb, skills)
        matched, _ = skill_overlap_details(anchor_skills, peer_skills)
        item = _public_job_item(job, {"embedding": emb, "skills": skills, "combined": combined}, matched)
        ranked.append((combined, item))

    ranked.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in ranked[:limit]]


def find_similar_candidates(
    candidate_agent: CandidateAgent,
    candidate_id: str,
    *,
    limit: int = 3,
) -> list[dict[str, Any]]:
    anchor = candidate_agent.get_by_id(candidate_id)
    if anchor is None or not anchor.embedding:
        return []

    anchor_vec = np.asarray(anchor.embedding, dtype=np.float32)
    anchor_skills = anchor.skills
    ranked: list[tuple[float, dict[str, Any]]] = []

    for profile in candidate_agent.list_profiles():
        if profile.id == candidate_id or not profile.embedding:
            continue
        emb = cosine_similarity(anchor_vec, np.asarray(profile.embedding, dtype=np.float32))
        skills = jaccard_skills(anchor_skills, profile.skills)
        combined = _combined_score(emb, skills)
        matched, _ = skill_overlap_details(anchor_skills, profile.skills)
        item = _public_candidate_item(
            profile,
            {"embedding": emb, "skills": skills, "combined": combined},
            matched,
        )
        ranked.append((combined, item))

    ranked.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in ranked[:limit]]
