"""ESCO-lite skill groups for taxonomy-aware overlap."""
from __future__ import annotations

from core.skill_catalog import canonical_skill

# Parent group -> member canonical skills
_TAXONOMY: dict[str, frozenset[str]] = {
    "programming": frozenset(
        {"python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "ruby", "php"}
    ),
    "ml_ai": frozenset(
        {
            "machine learning",
            "deep learning",
            "artificial intelligence",
            "natural language processing",
            "computer vision",
            "tensorflow",
            "pytorch",
            "scikit-learn",
        }
    ),
    "data": frozenset({"pandas", "numpy", "sql", "postgresql", "spark", "data visualization", "tableau", "power bi"}),
    "web_frontend": frozenset({"react", "vue", "angular", "html", "css", "figma", "ui/ux"}),
    "web_backend": frozenset({"node", "spring boot", "django", "flask", "fastapi", "rest api", "graphql"}),
    "devops_cloud": frozenset(
        {"docker", "kubernetes", "aws", "google cloud", "azure", "ci/cd", "terraform", "linux"}
    ),
    "mobile": frozenset({"android", "ios", "react native", "flutter", "kotlin", "swift"}),
}


def skill_groups(skills: list[str]) -> set[str]:
    canon = {canonical_skill(s) for s in skills}
    groups: set[str] = set()
    for group, members in _TAXONOMY.items():
        if canon & members:
            groups.add(group)
    return groups


def taxonomy_overlap(resume_skills: list[str], job_skills: list[str]) -> float:
    """Jaccard overlap on skill taxonomy groups."""
    a = skill_groups(resume_skills)
    b = skill_groups(job_skills)
    if not a and not b:
        return 0.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)
