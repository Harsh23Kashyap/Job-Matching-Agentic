from contracts.snapshots import CandidateSnapshot, JobSnapshot


def test_candidate_snapshot_immutable_fields():
    snap = CandidateSnapshot(
        id="cv_01",
        name="Rahul Sharma",
        skills=["Python"],
        experience_years=3,
        remote_preference=True,
        summary="ML engineer",
        version=1,
        document_text_hash="abc",
        embedding=[0.1, 0.2],
    )
    assert snap.name == "Rahul Sharma"
    assert snap.embedding == [0.1, 0.2]


def test_job_snapshot_required_skills():
    snap = JobSnapshot(
        id="job_01",
        title="Machine Learning Engineer",
        required_skills=["Python", "TensorFlow"],
        required_experience=2,
        remote_policy=True,
        description="ML role",
        version=1,
        document_text_hash="def",
        embedding=[0.3, 0.4],
    )
    assert "Python" in snap.required_skills
