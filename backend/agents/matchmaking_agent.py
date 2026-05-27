import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

import numpy as np

from agents.base import BaseAgent
from agents.candidate_agent import CandidateAgent
from agents.employer_agent import EmployerAgent
from bus.event_bus import AgentEventBus
from bus.events import AgentEvent, EventType
from config import Settings
from contracts.agent_status import AgentStatus
from contracts.matching import (
    DailyBatchRequest,
    DailyBatchResponse,
    EnsembleRequest,
    EnsembleSource,
    MatchRequest,
    MatchResponse,
    MatchResult,
    ScoreBreakdown,
)
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.rrf import rrf_fuse
from core.scoring import compute_multimodal_weighted, compute_semantic
from hooks.explainer import RuleExplainer


@dataclass
class MatchSession:
    session_id: str
    direction: str
    query_label: str


@dataclass
class MatchmakerAgentState:
    cache_valid: bool = True
    sessions: list[MatchSession] = field(default_factory=list)


class MatchmakingAgent(BaseAgent):
    agent_id = "matchmaking"
    display_name = "Matchmaking Agent"

    def __init__(
        self,
        bus: AgentEventBus,
        candidate_agent: CandidateAgent,
        employer_agent: EmployerAgent,
        explainer: RuleExplainer,
        settings: Settings,
    ) -> None:
        super().__init__()
        self.bus = bus
        self.candidate_agent = candidate_agent
        self.employer_agent = employer_agent
        self.explainer = explainer
        self.settings = settings
        self.state = MatchmakerAgentState()

    def register_handlers(self, bus: AgentEventBus) -> None:
        bus.subscribe(EventType.CANDIDATE_PROFILE_UPDATED, self._on_profile_updated)
        bus.subscribe(EventType.JOB_PROFILE_UPDATED, self._on_profile_updated)

    def _on_profile_updated(self, event: AgentEvent) -> None:
        self.state.cache_valid = False
        self._record_event(event.event_type.value, event.timestamp.isoformat())

    def _score_pair(
        self,
        candidate: CandidateSnapshot,
        job: JobSnapshot,
        strategy: str,
        metric: str,
        skills_mode: str,
        semantic_weight: float,
    ) -> ScoreBreakdown:
        if strategy == "semantic":
            return compute_semantic(candidate, job, metric)
        return compute_multimodal_weighted(
            candidate,
            job,
            metric=metric,
            semantic_weight=semantic_weight,
            skills_mode=skills_mode,
            model_name=self.settings.embedding_model,
        )

    def _rank_jobs_for_candidate(
        self,
        candidate: CandidateSnapshot,
        jobs: list[JobSnapshot],
        strategy: str,
        metric: str,
        skills_mode: str,
        semantic_weight: float,
        top_k: int,
    ) -> list[MatchResult]:
        scored: list[tuple[JobSnapshot, ScoreBreakdown]] = []
        for job in jobs:
            breakdown = self._score_pair(
                candidate, job, strategy, metric, skills_mode, semantic_weight
            )
            scored.append((job, breakdown))

        scored.sort(key=lambda x: x[1].final_score, reverse=True)
        results: list[MatchResult] = []
        for rank, (job, breakdown) in enumerate(scored[:top_k], start=1):
            results.append(
                MatchResult(
                    target_id=job.id,
                    target_label=job.title,
                    rank=rank,
                    similarity=breakdown.final_score,
                    semantic_score=breakdown.semantic_score,
                    skills_score=breakdown.skills_score,
                    why_ranked=self.explainer.explain(candidate, job, breakdown),
                )
            )
        return results

    def _rank_candidates_for_job(
        self,
        job: JobSnapshot,
        candidates: list[CandidateSnapshot],
        strategy: str,
        metric: str,
        skills_mode: str,
        semantic_weight: float,
        top_k: int,
    ) -> list[MatchResult]:
        scored: list[tuple[CandidateSnapshot, ScoreBreakdown]] = []
        for candidate in candidates:
            breakdown = self._score_pair(
                candidate, job, strategy, metric, skills_mode, semantic_weight
            )
            scored.append((candidate, breakdown))

        scored.sort(key=lambda x: x[1].final_score, reverse=True)
        results: list[MatchResult] = []
        for rank, (candidate, breakdown) in enumerate(scored[:top_k], start=1):
            results.append(
                MatchResult(
                    target_id=candidate.id,
                    target_label=candidate.name,
                    rank=rank,
                    similarity=breakdown.final_score,
                    semantic_score=breakdown.semantic_score,
                    skills_score=breakdown.skills_score,
                    why_ranked=self.explainer.explain(candidate, job, breakdown),
                )
            )
        return results

    def _agent_versions(self) -> dict[str, int]:
        return {
            "candidate": self.candidate_agent.state.store_version,
            "employer": self.employer_agent.state.store_version,
        }

    def _get_jobs_for_retrieval(
        self, request: MatchRequest, candidate: CandidateSnapshot
    ) -> list[JobSnapshot]:
        if request.retrieval == "ann":
            k = min(request.candidate_pool, len(self.employer_agent.list_jobs()))
            vec = np.asarray(candidate.embedding, dtype=np.float32)
            return self.employer_agent.search_jobs(vec, k)
        return [self.employer_agent.snapshot(j.id) for j in self.employer_agent.list_jobs()]

    def _get_candidates_for_retrieval(
        self, request: MatchRequest, job: JobSnapshot
    ) -> list[CandidateSnapshot]:
        if request.retrieval == "ann":
            k = min(request.candidate_pool, len(self.candidate_agent.list_profiles()))
            vec = np.asarray(job.embedding, dtype=np.float32)
            return self.candidate_agent.search_candidates(vec, k)
        return [
            self.candidate_agent.snapshot(c.id) for c in self.candidate_agent.list_profiles()
        ]

    def match_candidate_to_jobs(self, request: MatchRequest) -> MatchResponse:
        candidate = self.candidate_agent.get_by_name(request.query_key)
        if candidate is None:
            raise LookupError(f"Candidate not found: {request.query_key}")

        cand_snap = self.candidate_agent.snapshot(candidate.id)
        jobs = self._get_jobs_for_retrieval(request, cand_snap)
        session_id = str(uuid.uuid4())

        results = self._rank_jobs_for_candidate(
            cand_snap,
            jobs,
            request.strategy,
            request.metric,
            request.skills_mode,
            request.semantic_weight,
            request.top_k,
        )

        event = self.bus.make_event(
            EventType.MATCH_COMPLETED,
            self.agent_id,
            {"session_id": session_id, "direction": "candidate_to_jobs"},
        )
        self.bus.publish(event)
        self._record_event(event.event_type.value, event.timestamp.isoformat())
        self.state.sessions.append(
            MatchSession(session_id, "candidate_to_jobs", request.query_key)
        )
        if len(self.state.sessions) > 50:
            self.state.sessions = self.state.sessions[-50:]

        return MatchResponse(
            session_id=session_id,
            direction="candidate_to_jobs",
            query_label=candidate.name,
            strategy_used=request.strategy,
            results=results,
            corpus_size=len(self.employer_agent.list_jobs()),
            evaluated_count=len(jobs),
            agent_versions=self._agent_versions(),
        )

    def match_job_to_candidates(self, request: MatchRequest) -> MatchResponse:
        job = self.employer_agent.get_by_title(request.query_key)
        if job is None:
            raise LookupError(f"Job not found: {request.query_key}")

        job_snap = self.employer_agent.snapshot(job.id)
        candidates = self._get_candidates_for_retrieval(request, job_snap)
        session_id = str(uuid.uuid4())

        results = self._rank_candidates_for_job(
            job_snap,
            candidates,
            request.strategy,
            request.metric,
            request.skills_mode,
            request.semantic_weight,
            request.top_k,
        )

        event = self.bus.make_event(
            EventType.MATCH_COMPLETED,
            self.agent_id,
            {"session_id": session_id, "direction": "job_to_candidates"},
        )
        self.bus.publish(event)
        self._record_event(event.event_type.value, event.timestamp.isoformat())

        return MatchResponse(
            session_id=session_id,
            direction="job_to_candidates",
            query_label=job.title,
            strategy_used=request.strategy,
            results=results,
            corpus_size=len(self.candidate_agent.list_profiles()),
            evaluated_count=len(candidates),
            agent_versions=self._agent_versions(),
        )

    def match_ensemble(self, request: EnsembleRequest) -> MatchResponse:
        candidate = self.candidate_agent.get_by_name(request.query_key)
        if candidate is None:
            raise LookupError(f"Candidate not found: {request.query_key}")

        cand_snap = self.candidate_agent.snapshot(candidate.id)
        if request.retrieval == "ann":
            k = min(request.candidate_pool, len(self.employer_agent.list_jobs()))
            vec = np.asarray(cand_snap.embedding, dtype=np.float32)
            jobs = self.employer_agent.search_jobs(vec, k)
        else:
            jobs = [self.employer_agent.snapshot(j.id) for j in self.employer_agent.list_jobs()]

        runs: list[list[dict]] = []
        for search in request.searches:
            ranked = self._rank_jobs_for_candidate(
                cand_snap,
                jobs,
                search.strategy,
                search.metric,
                search.skills_mode,
                search.semantic_weight,
                len(jobs),
            )
            run_items = [
                {
                    "target_id": r.target_id,
                    "target_label": r.target_label,
                    "score": r.similarity,
                    "strategy": search.strategy,
                    "metric": search.metric,
                    "weight": search.weight,
                    "weight_used": search.weight,
                }
                for r in ranked
            ]
            runs.append(run_items)

        fused = rrf_fuse(runs, key_fn=lambda item: item["target_id"], base_k=self.settings.rrf_k)
        session_id = str(uuid.uuid4())

        results: list[MatchResult] = []
        job_by_id = {j.id: j for j in jobs}
        for rank, (target_id, _score, source_items) in enumerate(fused[: request.top_k], start=1):
            job = job_by_id[target_id]
            breakdown = self._score_pair(
                cand_snap,
                job,
                request.searches[0].strategy,
                request.searches[0].metric,
                request.searches[0].skills_mode,
                request.searches[0].semantic_weight,
            )
            sources = [
                EnsembleSource(
                    strategy=s["strategy"],
                    metric=s["metric"],
                    rank=s["rank"],
                    score=s["score"],
                    weight=s["weight"],
                    rrf_contribution=s["rrf_contribution"],
                )
                for s in source_items
            ]
            results.append(
                MatchResult(
                    target_id=target_id,
                    target_label=job.title,
                    rank=rank,
                    similarity=_score,
                    semantic_score=breakdown.semantic_score,
                    skills_score=breakdown.skills_score,
                    why_ranked=self.explainer.explain(cand_snap, job, breakdown),
                    sources=sources,
                )
            )

        return MatchResponse(
            session_id=session_id,
            direction="candidate_to_jobs",
            query_label=candidate.name,
            strategy_used="ensemble",
            results=results,
            corpus_size=len(self.employer_agent.list_jobs()),
            evaluated_count=len(jobs),
            agent_versions=self._agent_versions(),
        )

    def run_daily_batch(self, request: DailyBatchRequest) -> DailyBatchResponse:
        generated_at = datetime.now(timezone.utc).isoformat()
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        output_path = (
            self.settings.data_dir / f"daily_recommendations_{date_str}.json"
            if request.output_path is None
            else self.settings.repo_root / request.output_path
        )

        candidates = self.candidate_agent.list_profiles()
        if request.max_users > 0:
            candidates = candidates[: request.max_users]

        batch: dict = {"generated_at_utc": generated_at, "recommendations": {}}
        match_req = MatchRequest(
            query_key="",
            top_k=request.top_k,
            strategy=request.strategy,
            metric=request.metric,
            skills_mode=request.skills_mode,
            semantic_weight=request.semantic_weight,
            retrieval="ann",
            candidate_pool=request.candidate_pool,
        )

        for candidate in candidates:
            match_req = match_req.model_copy(update={"query_key": candidate.name})
            response = self.match_candidate_to_jobs(match_req)
            batch["recommendations"][candidate.name] = [
                {
                    "rank": r.rank,
                    "job_title": r.target_label,
                    "job_id": r.target_id,
                    "score": r.similarity,
                }
                for r in response.results
            ]

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(batch, indent=2), encoding="utf-8")

        return DailyBatchResponse(
            output_file=str(output_path),
            users_processed=len(candidates),
            generated_at_utc=generated_at,
        )

    def status(self) -> AgentStatus:
        return AgentStatus(
            agent_id=self.agent_id,
            display_name=self.display_name,
            entity_count=len(self.state.sessions),
            store_version=0,
            vector_store_backend="n/a",
            last_event=self.last_event,
            last_event_at=self.last_event_at,
            healthy=True,
        )
