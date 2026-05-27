import pytest

from core.resume_clean import clean_resume_text, resume_preview_excerpt


@pytest.mark.parametrize(
    "raw, forbidden",
    [
        ("Harsh Kashyap (cid:131) Python", "(cid:"),
        ("Skills (cid:239) Java (cid:1)", "(cid:"),
        ("Contact (cid:155) info", "(cid:"),
        ("Harsh Kashyap (cid:131), (cid:239), (cid:1), (cid:155)", "(cid:"),
        ("Skills § Java", "§"),
        ("Notes ¶ more", "¶"),
    ],
)
def test_removes_pdf_noise(raw, forbidden):
    cleaned = clean_resume_text(raw)
    assert forbidden not in cleaned


def test_removes_cid_comma_debris():
    raw = "Harsh Kashyap (cid:131), (cid:239), (cid:1), (cid:155)\nPython developer"
    cleaned = clean_resume_text(raw)
    assert cleaned == "Harsh Kashyap\nPython developer"


def test_preserves_name_and_skills():
    raw = "Harsh Kashyap\nSkills: Python, FastAPI, React"
    cleaned = clean_resume_text(raw)
    assert "Harsh Kashyap" in cleaned
    assert "Python" in cleaned
    assert "FastAPI" in cleaned


def test_preserves_email_phone_and_links():
    raw = """
    Harsh Kashyap (cid:131)
    harsh@example.com | +91 98765 43210
    https://linkedin.com/in/harsh-kashyap
    https://github.com/harshkashyap
    https://leetcode.com/u/harshkashyap
    https://harsh.dev
    Skills § Python
    """
    cleaned = clean_resume_text(raw)
    assert "harsh@example.com" in cleaned
    assert "98765" in cleaned
    assert "linkedin.com/in/harsh-kashyap" in cleaned
    assert "github.com/harshkashyap" in cleaned
    assert "leetcode.com/u/harshkashyap" in cleaned
    assert "harsh.dev" in cleaned
    assert "Python" in cleaned
    assert "(cid:" not in cleaned
    assert "§" not in cleaned


def test_collapses_repeated_spaces_and_blank_lines():
    raw = "Harsh   Kashyap\n\n\n\nPython    developer"
    cleaned = clean_resume_text(raw)
    assert "  " not in cleaned
    assert "\n\n\n" not in cleaned
    assert cleaned == "Harsh Kashyap\n\nPython developer"


def test_drops_punctuation_only_lines():
    raw = "Harsh Kashyap\n***\nPython"
    cleaned = clean_resume_text(raw)
    assert "***" not in cleaned
    assert "Harsh Kashyap" in cleaned
    assert "Python" in cleaned


def test_resume_preview_excerpt_truncates():
    raw = "A" * 600
    excerpt = resume_preview_excerpt(raw, limit=500)
    assert len(excerpt) == 501
    assert excerpt.endswith("…")


def test_empty_input():
    assert clean_resume_text("") == ""
    assert resume_preview_excerpt("") == ""


def test_fixes_hyphenated_line_breaks():
    raw = "Python develop-\ner with FastAPI"
    cleaned = clean_resume_text(raw)
    assert "develop-\ner" not in cleaned
    assert "developer" in cleaned.lower()


def test_removes_duplicate_lines():
    raw = "Harsh Kashyap\nHarsh Kashyap\nPython developer"
    cleaned = clean_resume_text(raw)
    assert cleaned.count("Harsh Kashyap") == 1


def test_joins_wrapped_lines():
    raw = "Built scalable backend services for\nmatching and ranking workflows."
    cleaned = clean_resume_text(raw)
    assert "workflows." in cleaned
    assert "\nmatching" not in cleaned
