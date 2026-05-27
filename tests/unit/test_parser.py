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
