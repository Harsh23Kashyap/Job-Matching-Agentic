from core.resume_clean import clean_resume_text
from core.resume_structured_extract import extract_structured_resume, merge_resume_extraction


RESUME_SAMPLE = """
Harsh Kashyap (cid:131), (cid:239)
harsh@example.com | +91 9876543210
https://linkedin.com/in/harsh-kashyap

SUMMARY
Machine learning engineer with 5 years of experience building Python services.

SKILLS
Python, FastAPI, React, Machine Learning, Docker

EXPERIENCE
Senior ML Engineer — Acme Corp
Jan 2020 - Present
Built ranking models and APIs.

EDUCATION
B.Tech Computer Science, IIT Delhi, 2019

PROJECTS
Job Matcher — Python, FastAPI, React
Built a composite scoring job search demo.
"""


def test_structured_resume_extracts_core_fields():
    cleaned = clean_resume_text(RESUME_SAMPLE)
    data = extract_structured_resume(cleaned)
    assert data["name"] == "Harsh Kashyap"
    assert data["email"] == "harsh@example.com"
    assert "python" in [skill.lower() for skill in data["skills"]]
    assert data["experience_years"] >= 5
    assert data["education"]
    assert data["projects"]
    assert "machine learning" in data["summary"].lower()


def test_merge_resume_extraction_prefers_llm_summary():
    rules = extract_structured_resume(clean_resume_text(RESUME_SAMPLE))
    llm = {
        "name": "Harsh Kashyap",
        "skills": ["Go"],
        "experience_years": 5,
        "summary": "Senior engineer focused on ML platforms and API design for hiring products.",
        "email": "",
        "phone": "",
        "linkedin": "",
        "portfolio": "",
        "other_links": [],
        "education": [],
        "projects": [],
        "remote_preference": False,
        "preferred_salary": None,
    }
    merged = merge_resume_extraction(rules, llm)
    assert "ML platforms" in merged["summary"]
    assert "python" in [skill.lower() for skill in merged["skills"]]
    assert "go" in [skill.lower() for skill in merged["skills"]]
