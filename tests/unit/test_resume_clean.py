import pytest

from core.resume_clean import clean_resume_text


def test_clean_cid_noise():
    raw = "Harsh Kashyap (cid:131) Python\n\n\nJava"
    assert "(cid:" not in clean_resume_text(raw)
    assert "Harsh Kashyap" in clean_resume_text(raw)


def test_clean_section_symbol():
    assert "§" not in clean_resume_text("Skills § Java")
