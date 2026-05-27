from typing import Literal

from pydantic import BaseModel, Field

Strategy = Literal["semantic", "multimodal"]
Metric = Literal["cosine", "euclidean"]
SkillsMode = Literal["jaccard", "embedding"]
RetrievalMode = Literal["exhaustive", "ann"]


class StrategyConfig(BaseModel):
    strategy: Strategy = "semantic"
    metric: Metric = "cosine"
    semantic_weight: float = 0.7
    skills_mode: SkillsMode = "jaccard"
    weight: float = 1.0


class MatchRequest(BaseModel):
    query_key: str
    top_k: int = Field(default=5, ge=1, le=50)
    strategy: Strategy = "semantic"
    metric: Metric = "cosine"
    skills_mode: SkillsMode = "jaccard"
    semantic_weight: float = 0.7
    retrieval: RetrievalMode = "exhaustive"
    candidate_pool: int = Field(default=120, ge=1)


class EnsembleSearchConfig(BaseModel):
    strategy: Strategy
    metric: Metric
    weight: float = 1.0
    skills_mode: SkillsMode = "jaccard"
    semantic_weight: float = 0.7


class EnsembleRequest(BaseModel):
    query_key: str
    top_k: int = 5
    searches: list[EnsembleSearchConfig] = Field(min_length=1)
    retrieval: RetrievalMode = "exhaustive"
    candidate_pool: int = 120


class ScoreBreakdown(BaseModel):
    semantic_score: float
    skills_score: float | None = None
    final_score: float
    strategy_used: str
    metric_used: str
    skills_mode_used: str | None = None


class EnsembleSource(BaseModel):
    strategy: str
    metric: str
    rank: int
    score: float
    weight: float
    rrf_contribution: float


class MatchResult(BaseModel):
    target_id: str
    target_label: str
    rank: int
    similarity: float
    semantic_score: float
    skills_score: float | None = None
    why_ranked: list[str] = Field(default_factory=list)
    sources: list[EnsembleSource] | None = None


class MatchResponse(BaseModel):
    session_id: str
    direction: Literal["candidate_to_jobs", "job_to_candidates"]
    query_label: str
    strategy_used: str
    results: list[MatchResult]
    corpus_size: int
    evaluated_count: int
    agent_versions: dict[str, int]


class DailyBatchRequest(BaseModel):
    top_k: int = 5
    strategy: Strategy = "semantic"
    metric: Metric = "cosine"
    skills_mode: SkillsMode = "jaccard"
    semantic_weight: float = 0.7
    candidate_pool: int = 120
    max_users: int = 0
    output_path: str | None = None


class DailyBatchResponse(BaseModel):
    output_file: str
    users_processed: int
    generated_at_utc: str
