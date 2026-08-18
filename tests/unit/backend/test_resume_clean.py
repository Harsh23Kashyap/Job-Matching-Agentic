import pytest

from core.resume_clean import clean_resume_text, resume_preview_excerpt


@pytest.mark.parametrize(
    "raw, forbidden",
    [
        ("Jordan Rivera (cid:131) Python", "(cid:"),
        ("Skills (cid:239) Java (cid:1)", "(cid:"),
        ("Contact (cid:155) info", "(cid:"),
        ("Jordan Rivera (cid:131), (cid:239), (cid:1), (cid:155)", "(cid:"),
        ("Skills § Java", "§"),
        ("Notes ¶ more", "¶"),
    ],
)
def test_removes_pdf_noise(raw, forbidden):
    cleaned = clean_resume_text(raw)
    assert forbidden not in cleaned


def test_removes_cid_comma_debris():
    raw = "Jordan Rivera (cid:131), (cid:239), (cid:1), (cid:155)\nPython developer"
    cleaned = clean_resume_text(raw)
    assert cleaned == "Jordan Rivera\nPython developer"


def test_preserves_name_and_skills():
    raw = "Jordan Rivera\nSkills: Python, FastAPI, React"
    cleaned = clean_resume_text(raw)
    assert "Jordan Rivera" in cleaned
    assert "Python" in cleaned
    assert "FastAPI" in cleaned


def test_preserves_email_phone_and_links():
    raw = """
    Jordan Rivera (cid:131)
    jordan@example.com | +91 98765 43210
    https://linkedin.com/in/jordan-rivera
    https://github.com/janedoe
    https://leetcode.com/u/janedoe
    https://jordan.dev
    Skills § Python
    """
    cleaned = clean_resume_text(raw)
    assert "jordan@example.com" in cleaned
    assert "98765" in cleaned
    assert "linkedin.com/in/jordan-rivera" in cleaned
    assert "github.com/janedoe" in cleaned
    assert "leetcode.com/u/janedoe" in cleaned
    assert "jordan.dev" in cleaned
    assert "Python" in cleaned
    assert "(cid:" not in cleaned
    assert "§" not in cleaned


def test_collapses_repeated_spaces_and_blank_lines():
    raw = "Jordan   Rivera\n\n\n\nPython    developer"
    cleaned = clean_resume_text(raw)
    assert "  " not in cleaned
    assert "\n\n\n" not in cleaned
    assert cleaned == "Jordan Rivera\n\nPython developer"


def test_drops_punctuation_only_lines():
    raw = "Jordan Rivera\n***\nPython"
    cleaned = clean_resume_text(raw)
    assert "***" not in cleaned
    assert "Jordan Rivera" in cleaned
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
    raw = "Jordan Rivera\nJordan Rivera\nPython developer"
    cleaned = clean_resume_text(raw)
    assert cleaned.count("Jordan Rivera") == 1


def test_joins_wrapped_lines():
    raw = "Built scalable backend services for\nmatching and ranking workflows."
    cleaned = clean_resume_text(raw)
    assert "workflows." in cleaned
    assert "\nmatching" not in cleaned
