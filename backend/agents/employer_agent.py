import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from agents.base import BaseAgent
from bus.event_bus import AgentEventBus
from config import Settings
from contracts.agent_status import AgentStatus
from contracts.profiles import JobProfile
from contracts.snapshots import JobSnapshot
from core.document_text import job_document_text
from core.embedding import embed_text
from hooks.parser import JsonParser
from stores.chroma_store import ChromaVectorStore


@dataclass
class EmployerAgentState:
    profiles: dict[str, JobProfile] = field(default_factory=dict)
    title_index: dict[str, str] = field(default_factory=dict)
    store_version: int = 0


class EmployerAgent(BaseAgent):
    agent_id = "employer"
    display_name = "Employer Agent"

    def __init__(
        self,
        bus: AgentEventBus,
        store: ChromaVectorStore,
        parser: JsonParser,
        settings: Settings,
    ) -> None:
        super().__init__()
        self.bus = bus
        self.store = store
        self.parser = parser
        self.settings = settings
        self.state = EmployerAgentState()

    def register(self, raw: dict) -> JobProfile:
        profile = self.parser.parse_job(raw)
        doc = job_document_text(raw)
        doc_hash = hashlib.sha256(doc.encode("utf-8")).hexdigest()
        vector = embed_text(doc, model_name=self.settings.embedding_model)

        existing = self.state.profiles.get(profile.id)
        version = (existing.version + 1) if existing else 1
        now = datetime.now(timezone.utc).isoformat()
        created_at = (existing.created_at if existing and existing.created_at else None) or profile.created_at or now

        profile = profile.model_copy(
            update={
                "version": version,
                "created_at": created_at,
                "updated_at": now,
                "document_text": doc,
                "document_text_hash": doc_hash,
                "embedding": vector.tolist(),
            }
        )

        self.store.upsert(
            profile.id,
            vector,
            {
                "id": profile.id,
                "title": profile.title,
                "company": profile.company or "",
                "required_skills": profile.required_skills,
            },
        )
        self.state.profiles[profile.id] = profile
        self.state.title_index[profile.title] = profile.id
        self.state.store_version += 1

        from bus.events import EventType

        event = self.bus.make_event(
            EventType.JOB_PROFILE_UPDATED,
            self.agent_id,
            {"job_id": profile.id, "version": version},
        )
        self.bus.publish(event)
        self._record_event(event.event_type.value, event.timestamp.isoformat())
        return profile

    def get_by_id(self, job_id: str) -> JobProfile | None:
        return self.state.profiles.get(job_id)

    def get_by_title(self, title: str) -> JobProfile | None:
        jid = self.state.title_index.get(title)
        return self.state.profiles.get(jid) if jid else None

    def list_titles(self) -> list[str]:
        return sorted(self.state.title_index.keys())

    def list_jobs(self) -> list[JobProfile]:
        return list(self.state.profiles.values())

    def snapshot(self, job_id: str) -> JobSnapshot:
        profile = self.state.profiles[job_id]
        if profile.embedding is None:
            raise ValueError(f"Job {job_id} has no embedding")
        return JobSnapshot(
            id=profile.id,
            title=profile.title,
            required_skills=profile.required_skills,
            preferred_skills=profile.preferred_skills,
            required_experience=profile.required_experience,
            remote_policy=profile.remote_policy,
            budget=profile.budget,
            description=profile.description,
            version=profile.version,
            document_text_hash=profile.document_text_hash,
            embedding=profile.embedding,
        )

    def search_jobs(self, query_vector: np.ndarray, k: int) -> list[JobSnapshot]:
        hits = self.store.search(query_vector, k)
        out: list[JobSnapshot] = []
        for hit in hits:
            if hit.entity_id in self.state.profiles:
                out.append(self.snapshot(hit.entity_id))
        return out

    def bootstrap_from_file(self, path: Path) -> int:
        raw_list = json.loads(path.read_text(encoding="utf-8"))
        for raw in raw_list:
            self.register(raw)
        return len(raw_list)

    def status(self) -> AgentStatus:
        return self._base_status(
            len(self.state.profiles),
            self.state.store_version,
            vector_store_backend=self.settings.vector_store,
        )
