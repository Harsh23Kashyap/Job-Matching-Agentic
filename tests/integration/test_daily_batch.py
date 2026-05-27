from contracts.matching import DailyBatchRequest
from core.explain import build_why_ranked
from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot


def test_daily_batch_writes_file(system, tmp_path):
    system.settings.data_dir = tmp_path
    req = DailyBatchRequest(top_k=2, max_users=2)
    resp = system.matchmaker.run_daily_batch(req)
    assert resp.users_processed == 2
    assert resp.output_file.endswith(".json")


def test_explain_includes_skill_overlap():
    cand = CandidateSnapshot(
        id="1",
        name="A",
        skills=["Python", "ML"],
        experience_years=1,
        remote_preference=True,
        summary="python ml engineer",
        version=1,
        document_text_hash="h",
        embedding=[1.0, 0.0],
    )
    job = JobSnapshot(
        id="2",
        title="ML Engineer",
        required_skills=["Python"],
        required_experience=1,
        remote_policy=True,
        description="d",
        version=1,
        document_text_hash="h2",
        embedding=[1.0, 0.0],
    )
    scores = ScoreBreakdown(
        semantic_score=0.7,
        skills_score=0.5,
        final_score=0.65,
        strategy_used="multimodal",
        metric_used="cosine",
        skills_mode_used="jaccard",
    )
    reasons = build_why_ranked(cand, job, scores)
    assert any("python" in r.lower() for r in reasons)
