from core.contact_extract import extract_contact_from_text, extract_name_from_text, merge_contact_fields


def test_extract_email_phone_linkedin():
    text = """
    Harsh Kashyap
    harsh@example.com | +91 98765 43210
    https://linkedin.com/in/harsh-kashyap
    """
    result = extract_contact_from_text(text)
    assert result["name"] == "Harsh Kashyap"
    assert result["email"] == "harsh@example.com"
    assert "98765" in result["phone"]
    assert "linkedin.com/in/harsh-kashyap" in result["linkedin"]


def test_extract_github_as_portfolio_when_only_link():
    text = "Contact: github.com/harshkashyap"
    result = extract_contact_from_text(text)
    assert result["portfolio"] == "https://github.com/harshkashyap"
    assert result["other_links"] == []


def test_extract_leetcode_in_other_links():
    text = "Profile: https://leetcode.com/u/harshkashyap"
    result = extract_contact_from_text(text)
    assert any("leetcode.com" in link for link in result["other_links"])


def test_extract_full_contact_block():
    text = """
    Harsh Kashyap (cid:131), (cid:239)
    harsh.kashyap@email.com | +91 9876543210
    https://linkedin.com/in/harsh-kashyap
    github.com/harshkashyap
    https://leetcode.com/u/harshkashyap
    https://harsh.dev
    https://www.credly.com/users/harsh-kashyap/badges
    """
    result = extract_contact_from_text(text)
    assert result["name"] == "Harsh Kashyap"
    assert result["email"] == "harsh.kashyap@email.com"
    assert "9876543210" in result["phone"]
    assert "linkedin.com/in/harsh-kashyap" in result["linkedin"]
    assert result["portfolio"] == "https://harsh.dev"
    assert any("github.com/harshkashyap" in link for link in result["other_links"])
    assert any("leetcode.com/u/harshkashyap" in link for link in result["other_links"])
    assert any("credly.com/users/harsh-kashyap" in link for link in result["other_links"])


def test_extract_name_skips_contact_lines():
    text = """
    harsh@example.com
    Harsh Kashyap
    """
    assert extract_name_from_text(text) == "Harsh Kashyap"


def test_merge_contact_fields_prefers_primary():
    primary = {
        "name": "Primary Name",
        "email": "primary@test.com",
        "phone": "",
        "linkedin": "",
        "portfolio": "",
        "other_links": [],
    }
    fallback = {
        "name": "Fallback Name",
        "email": "fallback@test.com",
        "phone": "+1 555",
        "linkedin": "",
        "portfolio": "",
        "other_links": ["https://x.com"],
    }
    merged = merge_contact_fields(primary, fallback)
    assert merged["name"] == "Primary Name"
    assert merged["email"] == "primary@test.com"
    assert merged["phone"] == "+1 555"
    assert merged["other_links"] == ["https://x.com"]


def test_merge_contact_fields_fills_missing_name():
    primary = {"name": "", "email": "", "phone": "", "linkedin": "", "portfolio": "", "other_links": []}
    fallback = {"name": "Harsh Kashyap", "email": "h@test.com", "phone": "", "linkedin": "", "portfolio": "", "other_links": []}
    merged = merge_contact_fields(primary, fallback)
    assert merged["name"] == "Harsh Kashyap"
    assert merged["email"] == "h@test.com"
