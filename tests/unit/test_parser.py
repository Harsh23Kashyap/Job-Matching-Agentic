from hooks.parser import JsonParser


def test_parse_candidate():
    p = JsonParser()
    profile = p.parse_candidate(
        {
            "id": "cv_01",
            "name": "Test",
            "skills": ["Python"],
            "experience_years": 2,
            "summary": "s",
        }
    )
    assert profile.name == "Test"
    assert profile.skills == ["Python"]
    assert profile.preferred_currency == "INR"
    assert profile.preferred_salary is None


def test_parse_candidate_normalizes_compensation():
    p = JsonParser()
    profile = p.parse_candidate(
        {
            "id": "cv_02",
            "name": "Test",
            "skills": ["Python"],
            "experience_years": 2,
            "summary": "s",
            "preferred_salary": "12,00,000",
            "preferred_currency": "usd",
        }
    )
    assert profile.preferred_salary == 1200000
    assert profile.preferred_currency == "USD"


def test_parse_job():
    p = JsonParser()
    profile = p.parse_job(
        {
            "id": "job_01",
            "title": "Engineer",
            "required_skills": ["Go"],
            "required_experience": 1,
            "description": "d",
        }
    )
    assert profile.title == "Engineer"
    assert profile.status == "open"
