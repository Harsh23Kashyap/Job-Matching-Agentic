from contracts.profiles import CandidateProfile, JobProfile
from core.resume_suggestions import (
    build_rule_based_suggestions,
    build_resume_suggestions,
    merge_llm_suggestions,
    missing_skills_for_job,
)


def _candidate() -> CandidateProfile:
    return CandidateProfile(
        id="cv_test",
        name="Rahul Sharma",
        skills=["Python", "Machine Learning", "AWS"],
        experience_years=3,
        summary="Machine learning engineer with 3 years experience in Python and AWS.",
    )


def _job() -> JobProfile:
    return JobProfile(
        id="job_01",
        title="Machine Learning Engineer",
        required_skills=["Python", "Machine Learning", "TensorFlow"],
        required_experience=2,
        description="Looking for ML engineer with strong Python and TensorFlow experience.",
        remote_policy=True,
    )


def test_missing_skills_detected():
    missing = missing_skills_for_job(_candidate(), _job())
    assert missing == ["TensorFlow"]


def test_rule_based_suggestions_shape():
    result = build_rule_based_suggestions(_candidate(), _job())
    assert result["job_id"] == "job_01"
    assert "TensorFlow" in result["missing_skills"]
    assert result["suggested_summary"]
    assert len(result["bullet_improvements"]) >= 1
    assert len(result["ats_checklist"]) >= 4
    assert all(row["status"] in {"pass", "warn", "fail"} for row in result["ats_checklist"])


def test_build_resume_suggestions_without_llm():
    result = build_resume_suggestions(_candidate(), _job(), llm=None)
    assert result["llm_status"] == "rule_based"
    assert "Suggestions only" in result["disclaimer"]


class _FakeLlm:
    def suggest_resume_for_job(self, _candidate, _job):
        return {
            "missing_keywords": ["TensorFlow", "Deep Learning"],
            "weak_skills": ["Machine Learning"],
            "missing_skills": ["TensorFlow"],
            "suggested_summary": "AI-tailored summary for ML Engineer role.",
            "bullet_improvements": [
                {
                    "original": "Built ML models in Python.",
                    "suggested": "Built ML models in Python and TensorFlow.",
                    "reason": "Add TensorFlow keyword.",
                }
            ],
            "ats_checklist": [
                {"item": "Keyword coverage", "status": "warn", "tip": "Add TensorFlow."},
            ],
        }


def test_build_resume_suggestions_with_llm():
    result = build_resume_suggestions(_candidate(), _job(), llm=_FakeLlm())
    assert result["llm_status"] == "ok"
    assert result["suggested_summary"].startswith("AI-tailored")
    assert result["bullet_improvements"][0]["suggested"].endswith("TensorFlow.")


def test_merge_llm_deduplicates_keywords():
    base = build_rule_based_suggestions(_candidate(), _job())
    merged = merge_llm_suggestions(
        base,
        {"missing_keywords": ["tensorflow", "Python", "Keras"], "missing_skills": [], "weak_skills": []},
    )
    lowered = [k.lower() for k in merged["missing_keywords"]]
    assert lowered.count("tensorflow") == 1
    assert lowered.count("python") == 1
