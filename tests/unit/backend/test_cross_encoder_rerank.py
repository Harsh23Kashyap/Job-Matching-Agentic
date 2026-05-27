"""Tests for two-stage cross-encoder reranking."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from bus.event_bus import AgentEventBus
from contracts.matching import MatchRequest
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.rerank_diagnostics import compute_rank_changes, top_k_ids


def test_compute_rank_changes():
    before = ["a", "b", "c"]
    after = ["b", "a", "c"]
    changes = compute_rank_changes(before, after, {"a": "A", "b": "B"}, top_k=3)
    assert len(changes) == 2
    assert any(c.target_id == "a" and c.rank_before == 1 and c.rank_after == 2 for c in changes)


def test_top_k_ids():
    rows = [("x", 1), ("y", 2), ("z", 3)]
    assert top_k_ids(rows, 2) == ["x", "y"]

    class Item:
        def __init__(self, id):
            self.id = id

    entity_rows = [(Item("a"), 1), (Item("b"), 2)]
    assert top_k_ids(entity_rows, 2) == ["a", "b"]


def test_cross_encoder_gated_by_config():
    from agents.matchmaking_agent import MatchmakingAgent
    from config import Settings
    from hooks.explainer import RuleExplainer

    settings = Settings(enable_cross_encoder_rerank=False)
    matchmaker = MatchmakingAgent(
        bus=AgentEventBus(),
        candidate_agent=MagicMock(),
        employer_agent=MagicMock(),
        explainer=RuleExplainer(),
        settings=settings,
    )
    request = MatchRequest(query_key="x", use_cross_encoder=True, top_k=3)
    assert matchmaker._cross_encoder_active(request) is False


@patch("agents.matchmaking_agent.rerank_jobs")
def test_two_stage_rerank_applied_when_enabled(mock_rerank):
    from agents.matchmaking_agent import MatchmakingAgent
    from config import Settings
    from contracts.profiles import CandidateProfile, JobProfile
    from hooks.explainer import RuleExplainer

    mock_rerank.return_value = [("job_b", 0.99), ("job_a", 0.5)]

    settings = Settings(enable_cross_encoder_rerank=True, cross_encoder_rerank_pool=20)
    candidate_agent = MagicMock()
    employer_agent = MagicMock()
    matchmaker = MatchmakingAgent(
        bus=AgentEventBus(),
        candidate_agent=candidate_agent,
        employer_agent=employer_agent,
        explainer=RuleExplainer(),
        settings=settings,
    )

    candidate = CandidateSnapshot(
        id="cv_01",
        name="Test",
        skills=["Python"],
        experience_years=1,
        remote_preference=False,
        summary="s",
        version=1,
        document_text_hash="h",
        embedding=[1.0, 0.0],
    )
    job_a = JobSnapshot(
        id="job_a",
        title="A",
        required_skills=["Python"],
        preferred_skills=[],
        required_experience=1,
        remote_policy=False,
        budget=None,
        description="a",
        version=1,
        document_text_hash="h1",
        embedding=[1.0, 0.0],
    )
    job_b = JobSnapshot(
        id="job_b",
        title="B",
        required_skills=["Java"],
        preferred_skills=[],
        required_experience=1,
        remote_policy=False,
        budget=None,
        description="b",
        version=1,
        document_text_hash="h2",
        embedding=[0.0, 1.0],
    )

    candidate_agent.get_by_id.return_value = CandidateProfile(
        id="cv_01", name="Test", skills=["Python"], experience_years=1, summary="s"
    )
    employer_agent.get_by_id.side_effect = lambda jid: JobProfile(
        id=jid,
        title=jid,
        required_skills=["Python"] if jid == "job_a" else ["Java"],
        required_experience=1,
        description="d",
    )

    request = MatchRequest(
        query_key="Test",
        top_k=2,
        strategy="semantic",
        use_cross_encoder=True,
        rerank_pool=20,
    )

    with patch.object(matchmaker, "_score_pair") as mock_score:
        from contracts.matching import ScoreBreakdown

        def score_side_effect(c, j, req, routing_reason=None):
            if j.id == "job_a":
                b = ScoreBreakdown(
                    semantic_score=0.9,
                    final_score=0.9,
                    strategy_used="semantic",
                    metric_used="cosine",
                )
            else:
                b = ScoreBreakdown(
                    semantic_score=0.1,
                    final_score=0.1,
                    strategy_used="semantic",
                    metric_used="cosine",
                )
            return b, []

        mock_score.side_effect = score_side_effect
        results, diag = matchmaker._rank_jobs_for_candidate(candidate, [job_a, job_b], request)

    assert mock_rerank.called
    assert diag is not None
    assert diag.applied is True
    assert diag.rerank_pool == 2
    assert results[0].target_id == "job_b"
