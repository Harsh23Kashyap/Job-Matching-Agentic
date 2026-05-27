from core.job_quality import analyze_job_quality


def test_strong_posting_scores_high():
    report = analyze_job_quality(
        {
            "title": "Senior Backend Engineer",
            "company": "Acme Labs",
            "location": "Bengaluru",
            "job_type": "Full-time",
            "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
            "required_experience": 6,
            "budget_currency": "INR",
            "budget_min": 2_000_000,
            "budget_max": 3_000_000,
            "remote_policy": True,
            "description": (
                "Build and maintain backend services for our hiring platform. "
                "You will design APIs, own PostgreSQL schemas, and deploy with Docker on AWS. "
                "6+ years of experience required."
            ),
        }
    )
    assert report["score"] >= 80
    assert report["grade"] == "strong"
    assert not report["missing_fields"]


def test_missing_fields_detected():
    report = analyze_job_quality({"title": "Engineer"})
    ids = {item["id"] for item in report["missing_fields"]}
    assert "missing_skills" in ids
    assert "missing_company" in ids
    assert report["score"] < 60


def test_salary_warning_for_low_budget():
    report = analyze_job_quality(
        {
            "title": "Senior Backend Engineer",
            "company": "Acme",
            "location": "Bengaluru",
            "required_skills": ["Python", "FastAPI", "Docker"],
            "required_experience": 7,
            "budget_currency": "INR",
            "budget_min": 400_000,
            "budget_max": 500_000,
            "description": "Build APIs and own backend delivery for platform teams with 7+ years experience.",
        }
    )
    assert any(item["id"] == "budget_low_for_experience" for item in report["salary_warnings"])


def test_experience_mismatch_senior_title():
    report = analyze_job_quality(
        {
            "title": "Senior Data Engineer",
            "company": "Acme",
            "location": "Remote",
            "required_skills": ["Python", "Spark", "SQL"],
            "required_experience": 2,
            "description": "Build data pipelines and own batch processing systems for analytics teams.",
        }
    )
    assert any(item["id"] == "senior_title_low_years" for item in report["experience_warnings"])


def test_skill_suggestions_from_title():
    report = analyze_job_quality(
        {
            "title": "Backend Engineer",
            "required_skills": ["Python"],
            "description": "Build services with FastAPI and deploy to production.",
        }
    )
    suggested = {skill.lower() for skill in report["skill_suggestions"]}
    assert "postgresql" in suggested or "docker" in suggested or "rest api" in suggested


def test_unclear_requirements_flags_vague_language():
    report = analyze_job_quality(
        {
            "title": "Software Engineer",
            "company": "Acme",
            "location": "Remote",
            "required_skills": ["Python", "Java", "Go"],
            "required_experience": 3,
            "description": "Looking for a team player with good communication in a fast-paced environment etc.",
        }
    )
    assert report["unclear_requirements"]
