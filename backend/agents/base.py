from contracts.agent_status import AgentStatus


class BaseAgent:
    agent_id: str = "base"
    display_name: str = "Base Agent"

    def __init__(self) -> None:
        self.last_event: str | None = None
        self.last_event_at: str | None = None

    def _record_event(self, event_type: str, timestamp_iso: str) -> None:
        self.last_event = event_type
        self.last_event_at = timestamp_iso

    def _base_status(
        self,
        entity_count: int,
        store_version: int,
        vector_store_backend: str = "chroma",
    ) -> AgentStatus:
        return AgentStatus(
            agent_id=self.agent_id,
            display_name=self.display_name,
            entity_count=entity_count,
            store_version=store_version,
            vector_store_backend=vector_store_backend,
            last_event=self.last_event,
            last_event_at=self.last_event_at,
            healthy=True,
        )
