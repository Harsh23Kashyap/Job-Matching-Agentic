"""Reindex in-memory profiles into vector stores after backend switch."""
from __future__ import annotations

from agents.candidate_agent import CandidateAgent
from agents.employer_agent import EmployerAgent
from bootstrap import SystemContainer
from config import Settings
from core.document_text import job_document_text, resume_document_text
from core.embedding import embed_text
from stores.factory import create_store


def _reindex_candidate_agent(agent: CandidateAgent, settings: Settings) -> None:
    agent.store = create_store(settings, "candidates_collection")
    agent.state.store_version = 0
    for profile in list(agent.state.profiles.values()):
        raw = profile.model_dump()
        doc = resume_document_text(raw)
        vector = embed_text(doc, model_name=settings.embedding_model)
        agent.store.upsert(
            profile.id,
            vector,
            {"id": profile.id, "name": profile.name, "skills": profile.skills},
        )
        agent.state.store_version += 1


def _reindex_employer_agent(agent: EmployerAgent, settings: Settings) -> None:
    agent.store = create_store(settings, "jobs_collection")
    agent.state.store_version = 0
    for profile in list(agent.state.profiles.values()):
        raw = profile.model_dump()
        doc = job_document_text(raw)
        vector = embed_text(doc, model_name=settings.embedding_model)
        agent.store.upsert(
            profile.id,
            vector,
            {"id": profile.id, "title": profile.title, "required_skills": profile.required_skills},
        )
        agent.state.store_version += 1


def switch_vector_store(container: SystemContainer, vector_store: str) -> dict:
    backend = vector_store.lower()
    if backend not in {"chroma", "qdrant"}:
        raise ValueError(f"Unsupported vector_store: {vector_store}")
    if backend == "qdrant":
        try:
            import qdrant_client  # noqa: F401
        except ImportError as exc:
            raise RuntimeError("qdrant-client is not installed") from exc

    container.settings.vector_store = backend
    _reindex_candidate_agent(container.candidate, container.settings)
    _reindex_employer_agent(container.employer, container.settings)
    return {
        "vector_store": backend,
        "candidates_reindexed": len(container.candidate.state.profiles),
        "jobs_reindexed": len(container.employer.state.profiles),
    }
