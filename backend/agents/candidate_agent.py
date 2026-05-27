import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from agents.base import BaseAgent
from bus.event_bus import AgentEventBus
from config import Settings
from contracts.agent_status import AgentStatus
from contracts.profiles import CandidateProfile
from contracts.snapshots import CandidateSnapshot
from core.document_text import resume_document_text
from core.embedding import embed_text
from hooks.parser import JsonParser
from stores.chroma_store import ChromaVectorStore


@dataclass
class CandidateAgentState:
    profiles: dict[str, CandidateProfile] = field(default_factory=dict)
    name_index: dict[str, str] = field(default_factory=dict)
    store_version: int = 0


class CandidateAgent(BaseAgent):
    agent_id = "candidate"
    display_name = "Candidate Agent"

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
        self.state = CandidateAgentState()

    def register(self, raw: dict) -> CandidateProfile:
        profile = self.parser.parse_candidate(raw)
        doc = resume_document_text(raw)
        doc_hash = hashlib.sha256(doc.encode("utf-8")).hexdigest()
        vector = embed_text(doc, model_name=self.settings.embedding_model)

        existing = self.state.profiles.get(profile.id)
        version = (existing.version + 1) if existing else 1

        profile = profile.model_copy(
            update={
                "version": version,
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
                "name": profile.name,
                "skills": profile.skills,
            },
        )
        self.state.profiles[profile.id] = profile
        self.state.name_index[profile.name] = profile.id
        self.state.store_version += 1

        from bus.events import EventType

        event = self.bus.make_event(
            EventType.CANDIDATE_PROFILE_UPDATED,
            self.agent_id,
            {"candidate_id": profile.id, "version": version},
        )
        self.bus.publish(event)
        self._record_event(event.event_type.value, event.timestamp.isoformat())
        return profile

    def get_by_id(self, candidate_id: str) -> CandidateProfile | None:
        return self.state.profiles.get(candidate_id)

    def get_by_name(self, name: str) -> CandidateProfile | None:
        cid = self.state.name_index.get(name)
        return self.state.profiles.get(cid) if cid else None

    def list_names(self) -> list[str]:
        return sorted(self.state.name_index.keys())

    def list_profiles(self) -> list[CandidateProfile]:
        return list(self.state.profiles.values())

    def snapshot(self, candidate_id: str) -> CandidateSnapshot:
        profile = self.state.profiles[candidate_id]
        if profile.embedding is None:
            raise ValueError(f"Candidate {candidate_id} has no embedding")
        return CandidateSnapshot(
            id=profile.id,
            name=profile.name,
            skills=profile.skills,
            experience_years=profile.experience_years,
            remote_preference=profile.remote_preference,
            preferred_salary=profile.preferred_salary,
            summary=profile.summary,
            version=profile.version,
            document_text_hash=profile.document_text_hash,
            embedding=profile.embedding,
        )

    def search_candidates(self, query_vector: np.ndarray, k: int) -> list[CandidateSnapshot]:
        hits = self.store.search(query_vector, k)
        out: list[CandidateSnapshot] = []
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
