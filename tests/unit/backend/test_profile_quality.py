from core.profile_quality import analyze_profile_quality


def test_strong_profile_scores_high():
    report = analyze_profile_quality(
        {
            "name": "Harsh Kashyap",
            "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"],
            "experience_years": 6,
            "preferred_salary": 2_500_000,
            "preferred_currency": "INR",
            "remote_preference": True,
            "summary": (
                "Backend engineer who built scalable APIs serving 2M+ requests/day. "
                "Led migration to FastAPI and reduced latency by 35%."
            ),
            "email": "harsh@example.com",
            "phone": "+91 9876543210",
            "linkedin": "https://linkedin.com/in/harsh",
        },
        llm_status="ok",
    )
    assert report["score"] >= 75
    assert report["completeness_percent"] >= 85
    assert report["parsing_confidence"]["level"] == "high"


def test_missing_fields_detected():
    report = analyze_profile_quality({"name": "Alex"})
    ids = {item["id"] for item in report["missing_fields"]}
    assert "missing_skills" in ids
    assert report["completeness_percent"] < 50


def test_summary_warnings_for_generic_text():
    report = analyze_profile_quality(
        {
            "name": "Alex",
            "skills": ["Python", "Java", "Go"],
            "experience_years": 4,
            "summary": "Hard-working team player and quick learner.",
        }
    )
    assert report["summary_warnings"]


def test_salary_guidance_when_missing():
    report = analyze_profile_quality(
        {
            "name": "Alex",
            "skills": ["Python", "SQL", "AWS"],
            "experience_years": 4,
            "summary": "Built data pipelines and owned ETL workflows for analytics teams.",
            "email": "alex@example.com",
        }
    )
    assert any(item["id"] == "salary_not_set" for item in report["salary_guidance"])


def test_parsing_confidence_manual_entry():
    report = analyze_profile_quality({"name": "Alex", "skills": ["Python"]})
    assert report["parsing_confidence"]["level"] == "manual"
    assert report["parsing_confidence"]["score"] is None


def test_skill_in_summary_flagged():
    report = analyze_profile_quality(
        {
            "name": "Alex",
            "skills": ["Java"],
            "experience_years": 3,
            "summary": "Backend developer with strong Python and FastAPI experience.",
        }
    )
    assert any("Python" in item["message"] for item in report["missing_skills"])
