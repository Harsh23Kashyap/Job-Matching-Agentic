from core.job_structured_extract import extract_structured_job, merge_job_extraction
from core.resume_clean import clean_resume_text


JD_SAMPLE = """
Senior Backend Engineer role with Python, FastAPI, and 5 years experience in Bengaluru.
Hybrid work. Full-time.

Requirements:
Python, FastAPI, PostgreSQL, Docker

Education:
B.Tech in Computer Science or equivalent
"""


def test_structured_job_extracts_title_skills_and_experience():
    cleaned = clean_resume_text(JD_SAMPLE)
    data = extract_structured_job(cleaned)
    assert data["title"] == "Senior Backend Engineer"
    assert data["required_experience"] == 5
    assert "python" in [skill.lower() for skill in data["required_skills"]]
    assert data["remote_policy"] is True
    assert data["education_requirements"]


def test_merge_job_extraction_prefers_llm_title():
    rules = extract_structured_job(clean_resume_text(JD_SAMPLE))
    llm = {
        "title": "Staff Backend Engineer",
        "required_skills": ["Kubernetes"],
        "required_experience": 6,
        "description": "Own platform APIs.",
        "company": "Acme",
        "location": "Bengaluru",
        "remote_policy": True,
        "job_type": "Full-time",
        "link": None,
        "budget_currency": "INR",
        "budget_min": 2000000,
        "budget_max": 3000000,
        "budget": 3000000,
        "education_requirements": [],
        "responsibilities": [],
    }
    merged = merge_job_extraction(rules, llm)
    assert merged["title"] == "Staff Backend Engineer"
    assert "kubernetes" in [skill.lower() for skill in merged["required_skills"]]
    assert "python" in [skill.lower() for skill in merged["required_skills"]]
