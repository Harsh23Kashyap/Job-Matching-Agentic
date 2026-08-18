"""EXP-023 / Stage-2 §F-G: deterministic synthetic corpus with TRANSPARENT latent ground truth.

Generates ~500 resumes + a job pool with structured attributes and a relevance label derived from a
KNOWN latent compatibility function (required/preferred skills, seniority, experience, family/title,
work-mode, compensation) — NOT from an LLM. The latent factors are stored so we can test whether the
ranking system RECOVERS known structure. Deterministic (seed) + versioned. Difficulty levels EASY/
MODERATE/HARD/ADVERSARIAL. Everything is labelled SYNTHETIC/CONTROLLED and must never be presented as
human recruitment judgments (Stage-2 §G/§I).

Run: PYTHONHASHSEED=0 python3 research/experiments/synthetic/generate_synthetic.py
Outputs to research/datasets/synthetic_v1/.
"""
from __future__ import annotations
import json
import random
from pathlib import Path

import os

# Backward-compatible defaults (synthetic_v1, 500x75) preserve reproduction of existing experiments;
# override via env for a larger corpus, e.g. SYNTH_VERSION=synthetic_v2 SYNTH_N_RESUMES=2000 SYNTH_N_JOBS=200.
VERSION = os.environ.get("SYNTH_VERSION", "synthetic_v1")
SEED = int(os.environ.get("SYNTH_SEED", "42"))
N_RESUMES = int(os.environ.get("SYNTH_N_RESUMES", "500"))
N_JOBS = int(os.environ.get("SYNTH_N_JOBS", "75"))
OUT = Path(__file__).resolve().parents[3] / "research" / "datasets" / VERSION

# 10 job families, each with a core skill pool + adjacent (shared) skills to create HARD overlaps.
FAMILIES = {
    "ml_engineering":  ["Machine Learning", "Deep Learning", "PyTorch", "Python", "MLOps", "Model Serving"],
    "data_science":    ["Statistics", "Python", "Pandas", "Experimentation", "SQL", "Data Visualization"],
    "data_engineering":["Spark", "Airflow", "SQL", "Kafka", "ETL", "Data Modeling"],
    "backend":         ["Java", "Microservices", "REST APIs", "SQL", "Distributed Systems", "Docker"],
    "frontend":        ["JavaScript", "React", "CSS", "TypeScript", "Accessibility", "Design Systems"],
    "mobile":          ["Kotlin", "Swift", "Android", "iOS", "Mobile Development", "REST APIs"],
    "devops":          ["Kubernetes", "Docker", "Terraform", "CI/CD", "AWS", "Observability"],
    "security":        ["Cybersecurity", "Threat Modeling", "Cryptography", "AppSec", "SIEM", "Python"],
    "product":         ["Product Strategy", "Roadmapping", "Analytics", "Stakeholder Mgmt", "SQL", "A/B Testing"],
    "design":          ["Figma", "UX Research", "Interaction Design", "Design Systems", "Prototyping", "Accessibility"],
}
FAM_KEYS = list(FAMILIES)
SENIORITY = ["junior", "mid", "senior", "staff"]          # index 0..3
SEN_YEARS = {"junior": (0, 2), "mid": (3, 5), "senior": (6, 9), "staff": (10, 15)}
WORK_MODES = ["remote", "hybrid", "onsite"]
LOCATIONS = ["NYC", "SF", "Remote-US", "London", "Bangalore", "Berlin"]

# transparent latent relevance weights (the KNOWN structure we test recovery of)
LW = {"required": 0.40, "preferred": 0.12, "seniority": 0.15, "experience": 0.13, "family": 0.10, "workmode": 0.05, "comp": 0.05}


def _skills_for(rng, fam, n, noise_families=0):
    pool = list(FAMILIES[fam])
    rng.shuffle(pool)
    sk = pool[:max(1, min(len(pool), n))]
    for _ in range(noise_families):  # inject adjacent-family skills (HARD overlap)
        other = rng.choice([f for f in FAM_KEYS if f != fam])
        sk.append(rng.choice(FAMILIES[other]))
    return sorted(set(sk))


def gen_resumes(rng):
    res = []
    for i in range(N_RESUMES):
        fam = FAM_KEYS[i % len(FAM_KEYS)] if i < len(FAM_KEYS) else rng.choice(FAM_KEYS)
        sen = rng.choice(SENIORITY)
        yr = rng.randint(*SEN_YEARS[sen])
        difficulty = rng.choices(["easy", "moderate", "hard", "adversarial"], weights=[0.35, 0.35, 0.2, 0.1])[0]
        noise = {"easy": 0, "moderate": 1, "hard": 2, "adversarial": 4}[difficulty]
        skills = _skills_for(rng, fam, rng.randint(3, 6), noise_families=noise)
        res.append({
            "id": f"scv_{i:04d}", "job_family": fam, "seniority": sen, "seniority_idx": SENIORITY.index(sen),
            "experience_years": yr, "skills": skills, "title": f"{sen.title()} {fam.replace('_', ' ').title()}",
            "education": rng.choice(["BS", "MS", "PhD", "Bootcamp"]),
            "preferred_salary": rng.choice([80, 100, 120, 150, 180, 220]) * 1000,
            "remote_preference": rng.choice([True, False]), "location": rng.choice(LOCATIONS),
            "difficulty": difficulty,
        })
    return res


def gen_jobs(rng):
    jobs = []
    for i in range(N_JOBS):
        fam = rng.choice(FAM_KEYS)
        req = _skills_for(rng, fam, rng.randint(2, 4))
        pref = _skills_for(rng, fam, rng.randint(1, 3))
        pref = [s for s in pref if s not in req]
        sen_target = rng.randint(1, 3)  # mid..staff
        jobs.append({
            "id": f"sjob_{i:03d}", "job_family": fam, "title": f"{SENIORITY[sen_target].title()} {fam.replace('_', ' ').title()}",
            "required_skills": req, "preferred_skills": pref,
            "required_experience_min": SEN_YEARS[SENIORITY[sen_target]][0],
            "required_experience_max": SEN_YEARS[SENIORITY[min(3, sen_target + 1)]][1],
            "seniority_target_idx": sen_target,
            "budget_min": rng.choice([80, 100, 120]) * 1000, "budget_max": rng.choice([150, 180, 220, 260]) * 1000,
            "work_mode": rng.choice(WORK_MODES), "location": rng.choice(LOCATIONS),
            "description": f"We are hiring a {SENIORITY[sen_target]} {fam.replace('_',' ')} engineer.",
        })
    return jobs


def latent_relevance(cv, job):
    cs, jr, jp = set(cv["skills"]), set(job["required_skills"]), set(job["preferred_skills"])
    required = len(cs & jr) / len(jr) if jr else 0.0
    preferred = len(cs & jp) / len(jp) if jp else 0.5
    lo, hi = job["required_experience_min"], job["required_experience_max"]
    experience = 1.0 if lo <= cv["experience_years"] <= hi else max(0.0, 1.0 - abs(cv["experience_years"] - (lo + hi) / 2) / 8.0)
    seniority = max(0.0, 1.0 - abs(cv["seniority_idx"] - job["seniority_target_idx"]) / 3.0)
    family = 1.0 if cv["job_family"] == job["job_family"] else 0.0
    workmode = 1.0 if (cv["remote_preference"] and job["work_mode"] == "remote") or (not cv["remote_preference"] and job["work_mode"] != "remote") else 0.4
    comp = 1.0 if job["budget_min"] <= cv["preferred_salary"] <= job["budget_max"] else 0.4
    factors = {"required": required, "preferred": preferred, "seniority": seniority,
               "experience": experience, "family": family, "workmode": workmode, "comp": comp}
    latent = sum(LW[k] * factors[k] for k in LW)
    return latent, factors


def to_grade(latent):
    return 3 if latent >= 0.80 else 2 if latent >= 0.60 else 1 if latent >= 0.40 else 0


def main():
    rng = random.Random(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    resumes, jobs = gen_resumes(rng), gen_jobs(rng)
    labels, noisy = [], random.Random(SEED + 1)
    for cv in resumes:
        for job in jobs:
            latent, factors = latent_relevance(cv, job)
            grade = to_grade(latent)
            noisy_grade = grade
            if noisy.random() < 0.08:  # 8% controlled label noise
                noisy_grade = max(0, min(3, grade + noisy.choice([-1, 1])))
            labels.append({"query_id": cv["id"], "doc_id": job["id"], "latent_score": round(latent, 4),
                           "latent_factors": {k: round(v, 3) for k, v in factors.items()},
                           "clean_grade": grade, "relevance": noisy_grade})
    pos = sum(1 for l in labels if l["relevance"] > 0)
    dist = {g: sum(1 for l in labels if l["relevance"] == g) for g in (0, 1, 2, 3)}
    (OUT / "synthetic_resumes.json").write_text(json.dumps(resumes, indent=1))
    (OUT / "synthetic_jobs.json").write_text(json.dumps(jobs, indent=1))
    (OUT / "synthetic_relevance.json").write_text(json.dumps(
        {"provenance": "SYNTHETIC / CONTROLLED — latent ground truth, NOT human judgments (Stage-2 §G/§I)",
         "labels": labels}, indent=1))
    manifest = {"version": VERSION, "seed": SEED, "n_resumes": N_RESUMES, "n_jobs": N_JOBS,
                "n_pairs": len(labels), "latent_weights": LW, "grade_thresholds": "3>=0.80,2>=0.60,1>=0.40",
                "label_noise": 0.08, "positive_pairs": pos, "grade_distribution": dist,
                "families": FAM_KEYS, "difficulty_levels": ["easy", "moderate", "hard", "adversarial"],
                "note": "Transparent latent-compatibility relevance. Recovery of this structure by the ranker is the test."}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
