from pydantic import BaseModel, Field


class CandidateProfile(BaseModel):
    id: str
    name: str
    skills: list[str]
    experience_years: float = Field(default=0, ge=0, le=50)
    preferred_salary: int | None = None
    preferred_currency: str = "INR"
    remote_preference: bool = False
    summary: str = ""
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    portfolio: str = ""
    other_links: list[str] = Field(default_factory=list)
    version: int = 1
    document_text: str = ""
    document_text_hash: str = ""
    embedding: list[float] | None = None


class JobProfile(BaseModel):
    id: str
    title: str
    required_skills: list[str]
    required_experience: int
    budget: int | None = None
    remote_policy: bool = False
    description: str = ""
    company: str | None = None
    location: str | None = None
    job_type: str | None = None
    link: str | None = None
    version: int = 1
    document_text: str = ""
    document_text_hash: str = ""
    embedding: list[float] | None = None
