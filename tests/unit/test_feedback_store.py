import pytest

from stores.feedback_store import FeedbackStore


@pytest.fixture
def store(tmp_path):
    return FeedbackStore(tmp_path / "feedback.db")


def test_record_user_action_and_list_latest(store):
    store.record_user_action(
        user_id="u1",
        target_id="job_01",
        action="save",
        role="candidate",
    )
    store.record_user_action(
        user_id="u1",
        target_id="job_01",
        action="not_interested",
        role="candidate",
    )
    rows = store.list_latest_for_user("u1")
    assert len(rows) == 1
    assert rows[0].target_id == "job_01"
    assert rows[0].action == "not_interested"


def test_list_latest_respects_context(store):
    store.record_user_action(
        user_id="u2",
        target_id="cv_01",
        action="save",
        role="employer",
        context_id="job_01",
    )
    store.record_user_action(
        user_id="u2",
        target_id="cv_01",
        action="reject",
        role="employer",
        context_id="job_02",
    )
    rows = store.list_latest_for_user("u2", context_id="job_01")
    assert len(rows) == 1
    assert rows[0].action == "save"
    assert rows[0].context_id == "job_01"


def test_match_feedback_still_records(store):
    store.record(candidate_id="cv_01", job_id="job_01", action="save", user_id="u1")
    counts = store.counts_for_pair("cv_01", "job_01")
    assert counts.save_count == 1


def test_user_feedback_persists_on_disk(tmp_path):
    db_path = tmp_path / "feedback_persist.db"
    store_a = FeedbackStore(db_path)
    store_a.record_user_action(
        user_id="persist-user",
        target_id="job_99",
        action="apply",
        role="candidate",
        context_id=None,
    )

    store_b = FeedbackStore(db_path)
    rows = store_b.list_latest_for_user("persist-user")
    assert len(rows) == 1
    assert rows[0].target_id == "job_99"
    assert rows[0].action == "apply"
    assert rows[0].role == "candidate"
