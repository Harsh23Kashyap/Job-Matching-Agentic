from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class EventType(str, Enum):
    CANDIDATE_PROFILE_UPDATED = "candidate.profile.updated"
    JOB_PROFILE_UPDATED = "job.profile.updated"
    CORPUS_BOOTSTRAPPED = "system.corpus.bootstrapped"
    MATCH_REQUESTED = "match.requested"
    MATCH_COMPLETED = "match.completed"


class AgentEvent(BaseModel):
    event_type: EventType
    timestamp: datetime
    publisher_id: str
    payload: dict
