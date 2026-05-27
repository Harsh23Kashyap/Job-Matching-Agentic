from core.contact_extract import extract_contact_from_text, merge_contact_fields


def test_extract_email_phone_linkedin():
    text = """
    Harsh Kashyap
    harsh@example.com | +91 98765 43210
    https://linkedin.com/in/harsh-kashyap
    """
    result = extract_contact_from_text(text)
    assert result["email"] == "harsh@example.com"
    assert "98765" in result["phone"]
    assert "linkedin.com/in/harsh-kashyap" in result["linkedin"]


def test_extract_github_as_portfolio():
    text = "Contact: https://github.com/harshkashyap"
    result = extract_contact_from_text(text)
    assert result["portfolio"] == "https://github.com/harshkashyap"


def test_extract_leetcode_in_other_links():
    text = "Profile: https://leetcode.com/u/harshkashyap"
    result = extract_contact_from_text(text)
    assert any("leetcode.com" in link for link in result["other_links"])


def test_merge_contact_fields_prefers_primary():
    primary = {"email": "primary@test.com", "phone": "", "linkedin": "", "portfolio": "", "other_links": []}
    fallback = {"email": "fallback@test.com", "phone": "+1 555", "linkedin": "", "portfolio": "", "other_links": ["https://x.com"]}
    merged = merge_contact_fields(primary, fallback)
    assert merged["email"] == "primary@test.com"
    assert merged["phone"] == "+1 555"
    assert merged["other_links"] == ["https://x.com"]
