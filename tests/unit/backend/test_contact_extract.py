from core.contact_extract import extract_contact_from_text, extract_name_from_text, merge_contact_fields


def test_extract_email_phone_linkedin():
    text = """
    Jordan Rivera
    jordan@example.com | +91 98765 43210
    https://linkedin.com/in/jordan-rivera
    """
    result = extract_contact_from_text(text)
    assert result["name"] == "Jordan Rivera"
    assert result["email"] == "jordan@example.com"
    assert "98765" in result["phone"]
    assert "linkedin.com/in/jordan-rivera" in result["linkedin"]


def test_extract_github_as_portfolio_when_only_link():
    text = "Contact: github.com/janedoe"
    result = extract_contact_from_text(text)
    assert result["portfolio"] == "https://github.com/janedoe"
    assert result["other_links"] == []


def test_extract_leetcode_in_other_links():
    text = "Profile: https://leetcode.com/u/janedoe"
    result = extract_contact_from_text(text)
    assert any("leetcode.com" in link for link in result["other_links"])


def test_extract_full_contact_block():
    text = """
    Jordan Rivera (cid:131), (cid:239)
    jordan.rivera@email.com | +91 9876543210
    https://linkedin.com/in/jordan-rivera
    github.com/janedoe
    https://leetcode.com/u/janedoe
    https://jordan.dev
    https://www.credly.com/users/jordan-rivera/badges
    """
    result = extract_contact_from_text(text)
    assert result["name"] == "Jordan Rivera"
    assert result["email"] == "jordan.rivera@email.com"
    assert "9876543210" in result["phone"]
    assert "linkedin.com/in/jordan-rivera" in result["linkedin"]
    assert result["portfolio"] == "https://jordan.dev"
    assert any("github.com/janedoe" in link for link in result["other_links"])
    assert any("leetcode.com/u/janedoe" in link for link in result["other_links"])
    assert any("credly.com/users/jordan-rivera" in link for link in result["other_links"])


def test_extract_name_skips_contact_lines():
    text = """
    jordan@example.com
    Jordan Rivera
    """
    assert extract_name_from_text(text) == "Jordan Rivera"


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
    fallback = {"name": "Jordan Rivera", "email": "h@test.com", "phone": "", "linkedin": "", "portfolio": "", "other_links": []}
    merged = merge_contact_fields(primary, fallback)
    assert merged["name"] == "Jordan Rivera"
    assert merged["email"] == "h@test.com"
