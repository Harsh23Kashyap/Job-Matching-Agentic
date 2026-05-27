from pydantic import BaseModel


class AgentStatus(BaseModel):
    agent_id: str
    display_name: str
    entity_count: int
    store_version: int
    vector_store_backend: str
    last_event: str | None = None
    last_event_at: str | None = None
    healthy: bool = True


class AgentsStatusResponse(BaseModel):
    candidate: AgentStatus
    employer: AgentStatus
    matchmaking: AgentStatus
