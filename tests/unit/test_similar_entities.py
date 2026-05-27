import pytest

from agents.candidate_agent import CandidateAgent
from agents.employer_agent import EmployerAgent
from bootstrap import create_system
from config import Settings
from core.similar_entities import find_similar_candidates, find_similar_jobs


@pytest.fixture
def agents_system(tmp_path, repo_root):
    settings = Settings(
        repo_root=repo_root,
        data_dir=repo_root / "data",
        chroma_persist_dir=tmp_path / "chroma",
        sqlite_path=tmp_path / "app.db",
    )
    return create_system(settings)


def test_find_similar_jobs_excludes_anchor_and_ranks(agents_system):
    employer: EmployerAgent = agents_system.employer
    items = find_similar_jobs(employer, "job_01", limit=3)
    assert len(items) <= 3
    assert all(item["id"] != "job_01" for item in items)
    assert all(0 <= item["similarity_score"] <= 1 for item in items)
    assert all("embedding_score" in item and "skills_score" in item for item in items)
    if len(items) >= 2:
        assert items[0]["similarity_score"] >= items[1]["similarity_score"]


def test_find_similar_jobs_ml_engineer_prefers_related_roles(agents_system):
    employer: EmployerAgent = agents_system.employer
    items = find_similar_jobs(employer, "job_01", limit=3)
    titles = [item["label"] for item in items]
    assert "Frontend Developer" not in titles[:1]


def test_find_similar_candidates_excludes_anchor(agents_system):
    candidate_agent: CandidateAgent = agents_system.candidate
    items = find_similar_candidates(candidate_agent, "cv_01", limit=3)
    assert len(items) <= 3
    assert all(item["id"] != "cv_01" for item in items)
    assert all(item["label"] for item in items)


def test_find_similar_unknown_anchor_returns_empty(agents_system):
    employer: EmployerAgent = agents_system.employer
    assert find_similar_jobs(employer, "missing", limit=3) == []


def test_similar_jobs_skill_overlap_present(agents_system):
    employer: EmployerAgent = agents_system.employer
    anchor = employer.get_by_id("job_01")
    items = find_similar_jobs(employer, "job_01", limit=1)
    if not items:
        pytest.skip("No peer jobs in corpus")
    peer = employer.get_by_id(items[0]["id"])
    shared = set(s.lower() for s in anchor.required_skills) & set(s.lower() for s in peer.required_skills)
    if shared:
        assert items[0]["matched_skills"]
