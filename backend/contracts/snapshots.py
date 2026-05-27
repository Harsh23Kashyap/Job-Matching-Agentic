from pydantic import BaseModel


class CandidateSnapshot(BaseModel):
    id: str
    name: str
    skills: list[str]
    experience_years: int
    remote_preference: bool
    summary: str
    version: int
    document_text_hash: str
    embedding: list[float]


class JobSnapshot(BaseModel):
    id: str
    title: str
    required_skills: list[str]
    required_experience: int
    remote_policy: bool
    description: str
    version: int
    document_text_hash: str
    embedding: list[float]
