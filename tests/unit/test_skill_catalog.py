from core.skill_catalog import (
    canonical_skill,
    canonicalize_skills,
    normalize_skill,
    normalize_skill_list,
    normalize_skills,
)
from core.skills import jaccard_skills, skill_overlap_details


def test_react_variants_map_to_react():
    assert canonical_skill("React.js") == "react"
    assert canonical_skill("ReactJS") == "react"
    assert normalize_skill("React.js").display == "React"


def test_spring_boot_variants():
    assert canonical_skill("SpringBoot") == "spring boot"
    assert normalize_skill("spring-boot").display == "Spring Boot"


def test_ci_cd_variants():
    assert canonical_skill("CICD") == "ci/cd"
    assert canonical_skill("CI CD") == "ci/cd"
    assert normalize_skill("cicd").display == "CI/CD"


def test_ml_maps_to_machine_learning():
    assert canonical_skill("ML") == "machine learning"
    assert normalize_skill("ml").display == "Machine Learning"


def test_aws_ec2_maps_to_aws():
    assert canonical_skill("AWS EC2") == "aws"
    assert canonical_skill("Amazon EC2") == "aws"
    assert normalize_skill("aws ec2").display == "AWS"


def test_normalize_skills_deduplicates_variants():
    entries = normalize_skills(["React.js", "React", "reactjs", "Python"])
    displays = [entry.display for entry in entries]
    assert displays == ["Python", "React"]
    assert len(entries) == 2


def test_normalize_skill_list_returns_display_names():
    assert normalize_skill_list(["fastapi", "FastAPI", "Python"]) == ["FastAPI", "Python"]


def test_canonicalize_skills_for_matching():
    assert canonicalize_skills(["React.js", "React"]) == ["react"]


def test_jaccard_treats_synonyms_as_overlap():
    score = jaccard_skills(["React.js"], ["React"])
    assert score == 1.0


def test_skill_overlap_details_uses_canonical_matching():
    matched, missing = skill_overlap_details(
        ["React.js", "AWS EC2"],
        ["React", "Python", "SpringBoot", "AWS"],
    )
    assert matched == ["AWS", "React"]
    assert missing == ["Python", "Spring Boot"]
