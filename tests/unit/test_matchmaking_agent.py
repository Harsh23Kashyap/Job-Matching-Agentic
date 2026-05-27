from unittest.mock import MagicMock

from bus.events import EventType
from bus.event_bus import AgentEventBus
from contracts.matching import MatchRequest
from contracts.snapshots import CandidateSnapshot, JobSnapshot


def _make_matchmaker():
    from agents.matchmaking_agent import MatchmakingAgent
    from config import Settings
    from hooks.explainer import RuleExplainer

    bus = AgentEventBus()
    candidate_agent = MagicMock()
    employer_agent = MagicMock()
    matchmaker = MatchmakingAgent(
        bus=bus,
        candidate_agent=candidate_agent,
        employer_agent=employer_agent,
        explainer=RuleExplainer(),
        settings=Settings(),
    )
    return matchmaker, bus, candidate_agent, employer_agent


def test_cache_invalidated_on_profile_update():
    matchmaker, bus, _, _ = _make_matchmaker()
    matchmaker.register_handlers(bus)
    assert matchmaker.state.cache_valid is True
    event = bus.make_event(
        EventType.CANDIDATE_PROFILE_UPDATED,
        "candidate",
        {"candidate_id": "cv_01"},
    )
    bus.publish(event)
    assert matchmaker.state.cache_valid is False


def test_match_candidate_to_jobs_ranks_by_score():
    matchmaker, _, candidate_agent, employer_agent = _make_matchmaker()

    from contracts.profiles import CandidateProfile, JobProfile

    candidate_agent.get_by_name.return_value = CandidateProfile(
        id="cv_01",
        name="Rahul Sharma",
        skills=["Python"],
        experience_years=1,
        summary="s",
    )
    candidate_agent.snapshot.return_value = CandidateSnapshot(
        id="cv_01",
        name="Rahul Sharma",
        skills=["Python"],
        experience_years=1,
        remote_preference=True,
        summary="s",
        version=1,
        document_text_hash="h",
        embedding=[1.0, 0.0],
    )
    employer_agent.list_jobs.return_value = [
        JobProfile(
            id="job_a",
            title="Job A",
            required_skills=["Python"],
            required_experience=1,
            description="a",
        ),
        JobProfile(
            id="job_b",
            title="Job B",
            required_skills=["Java"],
            required_experience=1,
            description="b",
        ),
    ]

    def snapshot(job_id):
        if job_id == "job_a":
            return JobSnapshot(
                id="job_a",
                title="Job A",
                required_skills=["Python"],
                required_experience=1,
                remote_policy=True,
                description="a",
                version=1,
                document_text_hash="h1",
                embedding=[1.0, 0.0],
            )
        return JobSnapshot(
            id="job_b",
            title="Job B",
            required_skills=["Java"],
            required_experience=1,
            remote_policy=False,
            description="b",
            version=1,
            document_text_hash="h2",
            embedding=[0.0, 1.0],
        )

    employer_agent.snapshot.side_effect = snapshot

    req = MatchRequest(query_key="Rahul Sharma", top_k=2, strategy="semantic", metric="cosine")
    response = matchmaker.match_candidate_to_jobs(req)
    assert response.results[0].target_label == "Job A"
    assert response.results[0].rank == 1
