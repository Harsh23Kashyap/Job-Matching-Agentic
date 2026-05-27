from pydantic import BaseModel, Field

JOB_STATUSES = frozenset({"open", "closed", "draft"})


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
    preferred_skills: list[str] = Field(default_factory=list)
    required_experience: float = Field(default=0, ge=0, le=50)
    budget: int | None = None
    budget_currency: str = "INR"
    budget_min: int | None = None
    budget_max: int | None = None
    remote_policy: bool = False
    description: str = ""
    company: str | None = None
    location: str | None = None
    job_type: str | None = None
    accepts_applications: bool = True
    link: str | None = None
    source: str | None = None
    posted_at: str | None = None
    status: str = "open"
    created_at: str = ""
    updated_at: str = ""
    version: int = 1
    document_text: str = ""
    document_text_hash: str = ""
    embedding: list[float] | None = None
