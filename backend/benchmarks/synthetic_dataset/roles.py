"""Role templates and labeling logic for synthetic research datasets."""
from __future__ import annotations

from core.skill_catalog import normalize

ROLES = (
    "backend",
    "frontend",
    "ml",
    "data",
    "devops",
    "mobile",
    "product",
    "design",
)

ROLE_SKILLS: dict[str, list[str]] = {
    "backend": [
        "Python",
        "Java",
        "Go",
        "Node.js",
        "Spring Boot",
        "PostgreSQL",
        "Microservices",
        "REST APIs",
        "Kafka",
        "Redis",
    ],
    "frontend": [
        "React",
        "TypeScript",
        "JavaScript",
        "CSS",
        "Vue",
        "Angular",
        "Webpack",
        "Web Performance",
        "HTML",
        "Next.js",
    ],
    "ml": [
        "Python",
        "Machine Learning",
        "TensorFlow",
        "PyTorch",
        "Deep Learning",
        "NLP",
        "Scikit-learn",
        "MLOps",
        "Computer Vision",
        "Transformers",
    ],
    "data": [
        "Python",
        "SQL",
        "Pandas",
        "dbt",
        "Airflow",
        "Data Modeling",
        "Power BI",
        "ETL",
        "Spark",
        "Statistics",
    ],
    "devops": [
        "Docker",
        "Kubernetes",
        "Terraform",
        "CI/CD",
        "AWS",
        "Linux",
        "Prometheus",
        "Helm",
        "Ansible",
        "Cloud Architecture",
    ],
    "mobile": [
        "Swift",
        "Kotlin",
        "React Native",
        "Flutter",
        "iOS",
        "Android",
        "Mobile Development",
        "Firebase",
        "UIKit",
        "Jetpack Compose",
    ],
    "product": [
        "Product Management",
        "Roadmapping",
        "Agile",
        "SQL",
        "User Research",
        "A/B Testing",
        "Jira",
        "Stakeholder Management",
        "Analytics",
        "OKRs",
    ],
    "design": [
        "Figma",
        "UI/UX",
        "Design Systems",
        "Prototyping",
        "User Research",
        "Wireframing",
        "Accessibility",
        "Visual Design",
        "Interaction Design",
        "Adobe XD",
    ],
}

ADJACENT_ROLES: dict[str, set[str]] = {
    "backend": {"devops", "data", "ml"},
    "frontend": {"mobile", "design"},
    "ml": {"data", "backend"},
    "data": {"ml", "backend", "product"},
    "devops": {"backend"},
    "mobile": {"frontend"},
    "product": {"design", "data"},
    "design": {"frontend", "product"},
}

ROLE_TITLES: dict[str, list[str]] = {
    "backend": ["Backend Engineer", "Senior Backend Developer", "API Engineer", "Platform Engineer"],
    "frontend": ["Frontend Developer", "React Engineer", "UI Engineer", "Web Developer"],
    "ml": ["Machine Learning Engineer", "ML Scientist", "Applied ML Engineer", "AI Engineer"],
    "data": ["Data Analyst", "Analytics Engineer", "Data Engineer", "BI Analyst"],
    "devops": ["DevOps Engineer", "SRE", "Cloud Engineer", "Infrastructure Engineer"],
    "mobile": ["Mobile Developer", "iOS Engineer", "Android Developer", "React Native Developer"],
    "product": ["Product Manager", "Technical Product Manager", "Associate PM", "Product Owner"],
    "design": ["UX Designer", "Product Designer", "UI/UX Designer", "Design Lead"],
}

FIRST_NAMES = [
    "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Quinn", "Avery",
    "Sam", "Jamie", "Robin", "Drew", "Cameron", "Skyler", "Reese", "Logan",
    "Priya", "Arjun", "Meera", "Rahul", "Neha", "Vikram", "Ananya", "Karan",
    "Emily", "James", "Maria", "David", "Sarah", "Michael", "Lisa", "Robert",
]

LAST_NAMES = [
    "Chen", "Patel", "Kim", "Nguyen", "Garcia", "Smith", "Johnson", "Williams",
    "Brown", "Martinez", "Lee", "Singh", "Sharma", "Kapoor", "Iyer", "Das",
    "Okafor", "Mueller", "Rossi", "Anderson", "Taylor", "Brooks", "Rivera", "Shah",
]

COMPANIES = [
    "Northstar Labs", "Bluebridge Tech", "Summit Analytics", "Horizon Systems",
    "Vertex AI", "Cloudline", "Dataforge", "Pixelcraft", "Launchpad IO", "Corestack",
]

RELEVANCE_LABELS = {
    0: "not relevant",
    1: "partial match",
    2: "good match",
    3: "strong match",
}


def skill_overlap_ratio(candidate_skills: list[str], required_skills: list[str]) -> tuple[float, list[str], list[str]]:
    req_norm = {normalize(s): s for s in required_skills}
    cand_norm = {normalize(s): s for s in candidate_skills}
    overlap_keys = set(req_norm) & set(cand_norm)
    matched = sorted({req_norm[k] for k in overlap_keys}, key=str.lower)
    missing = [req_norm[k] for k in req_norm if k not in overlap_keys]
    ratio = len(overlap_keys) / len(req_norm) if req_norm else 0.0
    return ratio, matched, missing


def _remote_compatible(candidate: dict, job: dict) -> bool:
    if candidate.get("remote_preference") and not job.get("remote_policy", True):
        return False
    return True


def _salary_compatible(candidate: dict, job: dict) -> bool:
    pref = candidate.get("preferred_salary")
    budget = job.get("budget")
    if pref is None or budget is None:
        return True
    return pref <= budget * 1.2


def label_pair(candidate: dict, job: dict) -> tuple[int, str]:
    """Return graded relevance 0–3 and human-readable rationale."""
    ratio, matched, missing = skill_overlap_ratio(candidate["skills"], job["required_skills"])
    role_c = candidate["role"]
    role_j = job["role"]
    same_role = role_c == role_j
    adjacent = role_j in ADJACENT_ROLES.get(role_c, set())

    exp_required = int(job.get("required_experience", 0))
    exp_years = float(candidate.get("experience_years", 0))
    exp_gap = exp_required - exp_years
    exp_meets = exp_gap <= 0
    exp_close = exp_gap <= 1

    remote_ok = _remote_compatible(candidate, job)
    salary_ok = _salary_compatible(candidate, job)

    parts: list[str] = []
    parts.append(f"Role: candidate={role_c}, job={role_j} ({'same' if same_role else 'adjacent' if adjacent else 'different'}).")
    parts.append(
        f"Skills: {len(matched)}/{len(job['required_skills'])} required matched"
        + (f" ({', '.join(matched[:4])})" if matched else "")
        + (f"; missing: {', '.join(missing[:3])}" if missing else "")
        + "."
    )

    if exp_meets:
        parts.append(f"Experience: {exp_years:g}y meets {exp_required}y requirement.")
    elif exp_close:
        parts.append(f"Experience: {exp_years:g}y is slightly below {exp_required}y requirement.")
    else:
        parts.append(f"Experience: {exp_years:g}y below {exp_required}y requirement by {exp_gap:g}y.")

    if not remote_ok:
        parts.append("Remote/on-site preference mismatch.")
    if not salary_ok:
        parts.append("Salary expectation above job budget.")

    if same_role and ratio >= 0.75 and exp_meets and remote_ok and salary_ok:
        relevance = 3
    elif same_role and ratio >= 0.5 and exp_close and remote_ok:
        relevance = 2
    elif (same_role or adjacent) and ratio >= 0.34:
        relevance = 2 if exp_close and remote_ok else 1
    elif ratio >= 0.25 or (adjacent and matched):
        relevance = 1
    else:
        relevance = 0

    if relevance == 0 and ratio > 0:
        relevance = 1
        parts.append("Minimal skill overlap only.")

    parts.append(f"Label: {relevance} ({RELEVANCE_LABELS[relevance]}).")
    return relevance, " ".join(parts)
