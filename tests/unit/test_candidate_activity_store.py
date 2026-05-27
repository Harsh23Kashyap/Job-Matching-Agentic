import pytest

from stores.candidate_activity_store import CandidateActivityStore


@pytest.fixture
def store(tmp_path):
    return CandidateActivityStore(tmp_path / "activity.db")


def test_save_and_unsave_job(store):
    row = store.save_job("cv_01", "job_01", "ML Engineer")
    assert row.job_id == "job_01"
    assert store.is_saved("cv_01", "job_01")
    assert store.unsave_job("cv_01", "job_01")
    assert not store.is_saved("cv_01", "job_01")


def test_apply_idempotent(store):
    first = store.apply(
        candidate_id="cv_01",
        candidate_name="Alice",
        job_id="job_01",
        job_title="ML Engineer",
        match_score=0.88,
    )
    second = store.apply(
        candidate_id="cv_01",
        candidate_name="Alice",
        job_id="job_01",
        job_title="ML Engineer",
        match_score=0.9,
    )
    assert first.id == second.id
    apps = store.list_applications_for_candidate("cv_01")
    assert len(apps) == 1


def test_list_applications_for_jobs(store):
    store.apply(candidate_id="cv_01", candidate_name="Alice", job_id="job_01", job_title="A")
    store.apply(candidate_id="cv_02", candidate_name="Bob", job_id="job_01", job_title="A")
    rows = store.list_applications_for_jobs(["job_01"])
    assert len(rows) == 2
