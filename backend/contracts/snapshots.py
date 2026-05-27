from pydantic import BaseModel, Field


class CandidateSnapshot(BaseModel):
    id: str
    name: str
    skills: list[str]
    experience_years: float
    remote_preference: bool
    preferred_salary: int | None = None
    summary: str
    version: int
    document_text_hash: str
    embedding: list[float]


class JobSnapshot(BaseModel):
    id: str
    title: str
    required_skills: list[str]
    preferred_skills: list[str] = Field(default_factory=list)
    required_experience: int
    remote_policy: bool
    budget: int | None = None
    budget_min: int | None = None
    budget_max: int | None = None
    description: str
    version: int
    document_text_hash: str
    embedding: list[float]
