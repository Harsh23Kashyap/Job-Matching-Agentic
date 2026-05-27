from core.skills import skill_overlap_details


def test_skill_overlap_details():
    matched, missing = skill_overlap_details(
        ["Python", "AWS"],
        ["Python", "Java", "Spring Boot"],
    )
    assert matched == ["Python"]
    assert missing == ["Java", "Spring Boot"]


def test_skill_overlap_details_case_insensitive():
    matched, missing = skill_overlap_details(["python"], ["Python", "Go"])
    assert matched == ["Python"]
    assert missing == ["Go"]
