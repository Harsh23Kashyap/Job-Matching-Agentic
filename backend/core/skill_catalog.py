_SYNONYMS = {
    "react.js": "react",
    "reactjs": "react",
    "react js": "react",
    "node.js": "node",
    "nodejs": "node",
    "vue.js": "vue",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "torch": "pytorch",
    "tf": "tensorflow",
    "k8s": "kubernetes",
    "kube": "kubernetes",
    "aws lambda": "aws",
    "amazon web services": "aws",
    "gcp": "google cloud",
    "google cloud platform": "google cloud",
    "js": "javascript",
    "ts": "typescript",
    "postgres": "postgresql",
    "powerbi": "power bi",
    "ci cd": "ci/cd",
    "cicd": "ci/cd",
    "ui ux": "ui/ux",
    "uiux": "ui/ux",
    "figma design": "figma",
    "springboot": "spring boot",
    "spring-boot": "spring boot",
    "data viz": "data visualization",
    "data visualisation": "data visualization",
    "micro services": "microservices",
    "sys design": "system design",
}


def normalize(skill: str) -> str:
    return skill.strip().lower()


def canonical_skill(skill: str) -> str:
    key = normalize(skill)
    return _SYNONYMS.get(key, key)


def canonicalize_skills(skills: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for skill in skills:
        canon = canonical_skill(skill)
        if canon and canon not in seen:
            seen.add(canon)
            out.append(canon)
    return sorted(out)
