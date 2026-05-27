"""Generate synthetic research evaluation corpus (candidates, jobs, labeled pairs)."""
from __future__ import annotations

import json
import random
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from benchmarks.synthetic_dataset.roles import (
    ADJACENT_ROLES,
    COMPANIES,
    FIRST_NAMES,
    LAST_NAMES,
    ROLES,
    ROLE_SKILLS,
    ROLE_TITLES,
    label_pair,
)


@dataclass
class SyntheticDatasetConfig:
    num_candidates: int = 100
    num_jobs: int = 50
    seed: int = 42
    id_prefix_candidate: str = "rcv"
    id_prefix_job: str = "rjob"
    full_pair_matrix: bool = True


def _pick_skills(rng: random.Random, role: str, count: int) -> list[str]:
    pool = ROLE_SKILLS[role]
    return rng.sample(pool, k=min(count, len(pool)))


def _salary_for_role(rng: random.Random, role: str, experience: float) -> int:
    base = {
        "backend": 115000,
        "frontend": 95000,
        "ml": 140000,
        "data": 105000,
        "devops": 130000,
        "mobile": 110000,
        "product": 120000,
        "design": 90000,
    }[role]
    return int(base + experience * 8000 + rng.randint(-5000, 15000))


def _budget_for_role(rng: random.Random, role: str, experience: int) -> int:
    base = {
        "backend": 125000,
        "frontend": 100000,
        "ml": 150000,
        "data": 110000,
        "devops": 140000,
        "mobile": 115000,
        "product": 125000,
        "design": 95000,
    }[role]
    return int(base + experience * 7000 + rng.randint(0, 20000))


def _summary_for(role: str, skills: list[str], experience: float) -> str:
    lead = skills[0] if skills else role
    return (
        f"{ROLE_TITLES[role][0].split()[0]} professional with {experience:g} years experience "
        f"in {lead} and related {role} tooling."
    )


def _job_description(role: str, title: str, skills: list[str], experience: int) -> str:
    return (
        f"We are hiring a {title} to build {role} capabilities. "
        f"Required skills include {', '.join(skills)}. "
        f"Minimum experience: {experience} years."
    )


def _assign_roles(count: int, rng: random.Random) -> list[str]:
    """Distribute items evenly across 8 role families."""
    per_role = count // len(ROLES)
    remainder = count % len(ROLES)
    roles: list[str] = []
    for i, role in enumerate(ROLES):
        n = per_role + (1 if i < remainder else 0)
        roles.extend([role] * n)
    rng.shuffle(roles)
    return roles


def generate_candidates(config: SyntheticDatasetConfig, rng: random.Random) -> list[dict[str, Any]]:
    role_assignments = _assign_roles(config.num_candidates, rng)
    candidates: list[dict[str, Any]] = []
    for idx, role in enumerate(role_assignments, start=1):
        experience = round(rng.uniform(1.0, 10.0), 1)
        skill_count = rng.randint(4, 6)
        skills = _pick_skills(rng, role, skill_count)
        # occasional cross-role skill for partial-match variety
        if rng.random() < 0.2:
            other = rng.choice([r for r in ROLES if r != role])
            skills.append(rng.choice(ROLE_SKILLS[other]))

        name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
        cid = f"{config.id_prefix_candidate}_{idx:03d}"
        candidates.append(
            {
                "id": cid,
                "name": name,
                "role": role,
                "skills": skills,
                "experience_years": experience,
                "preferred_salary": _salary_for_role(rng, role, experience),
                "remote_preference": rng.random() < 0.65,
                "summary": _summary_for(role, skills, experience),
            }
        )
    return candidates


def generate_jobs(config: SyntheticDatasetConfig, rng: random.Random) -> list[dict[str, Any]]:
    role_assignments = _assign_roles(config.num_jobs, rng)
    jobs: list[dict[str, Any]] = []
    title_counters: dict[str, int] = {r: 0 for r in ROLES}

    for idx, role in enumerate(role_assignments, start=1):
        title_pool = ROLE_TITLES[role]
        title = title_pool[title_counters[role] % len(title_pool)]
        title_counters[role] += 1

        required_experience = rng.randint(1, 7)
        req_count = rng.randint(3, 5)
        required_skills = _pick_skills(rng, role, req_count)
        preferred = _pick_skills(rng, role, rng.randint(0, 2))
        preferred = [s for s in preferred if s not in required_skills]

        jid = f"{config.id_prefix_job}_{idx:03d}"
        jobs.append(
            {
                "id": jid,
                "title": title,
                "role": role,
                "company": rng.choice(COMPANIES),
                "required_skills": required_skills,
                "preferred_skills": preferred,
                "required_experience": required_experience,
                "budget": _budget_for_role(rng, role, required_experience),
                "remote_policy": rng.random() < 0.6,
                "description": _job_description(role, title, required_skills, required_experience),
            }
        )
    return jobs


def generate_labels(
    candidates: list[dict[str, Any]],
    jobs: list[dict[str, Any]],
    *,
    full_matrix: bool = True,
    rng: random.Random,
) -> list[dict[str, Any]]:
    labels: list[dict[str, Any]] = []
    job_ids = [j["id"] for j in jobs]

    for candidate in candidates:
        targets = job_ids if full_matrix else _sample_jobs_for_candidate(candidate, jobs, rng)
        for job in jobs:
            if job["id"] not in targets:
                continue
            relevance, rationale = label_pair(candidate, job)
            labels.append(
                {
                    "query_id": candidate["id"],
                    "doc_id": job["id"],
                    "relevance": relevance,
                    "rationale": rationale,
                }
            )
    return labels


def _sample_jobs_for_candidate(
    candidate: dict[str, Any],
    jobs: list[dict[str, Any]],
    rng: random.Random,
) -> set[str]:
    """Sparse labels: same-role jobs + adjacent + random negatives."""
    role = candidate["role"]
    same = [j["id"] for j in jobs if j["role"] == role]
    adjacent_roles = ADJACENT_ROLES.get(role, set())
    adj = [j["id"] for j in jobs if j["role"] in adjacent_roles]
    other = [j["id"] for j in jobs if j["role"] != role and j["role"] not in adjacent_roles]
    picked = set(same)
    picked.update(rng.sample(adj, k=min(len(adj), 4)))
    picked.update(rng.sample(other, k=min(len(other), 6)))
    return picked


def generate_dataset(config: SyntheticDatasetConfig | None = None) -> dict[str, Any]:
    config = config or SyntheticDatasetConfig()
    rng = random.Random(config.seed)

    candidates = generate_candidates(config, rng)
    jobs = generate_jobs(config, rng)
    labels = generate_labels(candidates, jobs, full_matrix=config.full_pair_matrix, rng=rng)

    rel_counts = {0: 0, 1: 0, 2: 0, 3: 0}
    for label in labels:
        rel_counts[int(label["relevance"])] = rel_counts.get(int(label["relevance"]), 0) + 1

    role_counts_candidates = {r: sum(1 for c in candidates if c["role"] == r) for r in ROLES}
    role_counts_jobs = {r: sum(1 for j in jobs if j["role"] == r) for r in ROLES}

    return {
        "manifest": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "synthetic": True,
            "purpose": "research_evaluation",
            "seed": config.seed,
            "candidates": len(candidates),
            "jobs": len(jobs),
            "labeled_pairs": len(labels),
            "relevance_scale": "0-3",
            "roles": list(ROLES),
            "role_distribution_candidates": role_counts_candidates,
            "role_distribution_jobs": role_counts_jobs,
            "relevance_distribution": rel_counts,
            "full_pair_matrix": config.full_pair_matrix,
        },
        "candidates": candidates,
        "jobs": jobs,
        "eval_pairs": {
            "version": "1.0",
            "task": "resume_to_jobs",
            "relevance_scale": "0-3",
            "notes": (
                "Synthetic research corpus. relevance=3 strong, 2 good, 1 partial, 0 not relevant. "
                "Each label includes an auto-generated rationale from skill/role/experience rules."
            ),
            "labels": labels,
        },
    }


def write_dataset(out_dir: Path, dataset: dict[str, Any]) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "manifest": out_dir / "manifest.json",
        "candidates": out_dir / "cvs.json",
        "jobs": out_dir / "jobs.json",
        "eval_pairs": out_dir / "eval_pairs.json",
    }
    paths["manifest"].write_text(json.dumps(dataset["manifest"], indent=2), encoding="utf-8")
    paths["candidates"].write_text(json.dumps(dataset["candidates"], indent=2), encoding="utf-8")
    paths["jobs"].write_text(json.dumps(dataset["jobs"], indent=2), encoding="utf-8")
    paths["eval_pairs"].write_text(json.dumps(dataset["eval_pairs"], indent=2), encoding="utf-8")
    return paths
