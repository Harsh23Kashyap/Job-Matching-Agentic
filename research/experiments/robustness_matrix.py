"""EXP-029 / Stage-2 §R: robustness matrix over controlled resume perturbations.

For each perturbation type, perturb every resume, re-rank the 15 jobs, and measure vs baseline:
  - mean |Δ composite| on the resume's top job
  - top-1 stability (fraction of resumes whose #1 job is unchanged)
  - top-5 Jaccard (overlap of the top-5 job set before/after)
Desired behavior differs by type: synonym/capitalization/formatting should be INVARIANT
(Δ≈0, stability≈1); keyword-stuffing / irrelevant-skill injection should NOT dramatically
raise the score (robustness); skill-deletion / sparsity SHOULD reduce fit (sensitivity).

Run: cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false \
  PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/robustness_matrix.py
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import numpy as np


def _stable_offset(text: str) -> int:
    """Deterministic per-id offset (sha256), NOT Python hash() which is salted per process (audit B3)."""
    return int(hashlib.sha256(text.encode()).hexdigest(), 16) % 1000

from config import Settings
from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot
from benchmarks.extended_evaluation import load_settings_data
from core.scoring import compute_composite

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "research" / "results" / "robustness_matrix.json"
SEED = 42
MODEL = "all-MiniLM-L6-v2"

SYNONYMS = {"machine learning": "ML", "javascript": "JS", "kubernetes": "K8s",
            "postgresql": "Postgres", "typescript": "TS", "artificial intelligence": "AI",
            "natural language processing": "NLP", "continuous integration": "CI"}
IRRELEVANT = ["Underwater Basket Weaving", "Competitive Yodeling", "Medieval History", "Taxidermy"]


def misspell(s: str) -> str:
    return s[:-1] + s[-1] * 2 if len(s) > 3 else s + "x"  # simple deterministic typo


def perturb(cv: dict, kind: str, rng, catalog_skills):
    c = copy.deepcopy(cv)
    sk = list(c.get("skills", []))
    if kind == "skill_deletion" and sk:
        c["skills"] = sk[1:]
    elif kind == "irrelevant_skill_insertion":
        c["skills"] = sk + [IRRELEVANT[0]]
    elif kind == "keyword_stuffing":
        extra = list(rng.choice(catalog_skills, size=min(10, len(catalog_skills)), replace=False))
        c["skills"] = sk + [str(x) for x in extra]
    elif kind == "synonym_substitution":
        c["skills"] = [SYNONYMS.get(s.lower(), s) for s in sk]
    elif kind == "misspelling":
        c["skills"] = [misspell(s) for s in sk]
    elif kind == "capitalization":
        c["skills"] = [s.upper() for s in sk]
        c["summary"] = str(c.get("summary", "")).upper()
    elif kind == "formatting_noise":
        c["skills"] = [f"  {s}.,  " for s in sk]
    elif kind == "missing_compensation":
        c["preferred_salary"] = None
    elif kind == "missing_remote":
        c["remote_preference"] = not bool(c.get("remote_preference", False))
    elif kind == "sparse_resume":
        c["skills"] = sk[:1]
        c["summary"] = ""
    elif kind == "summary_removal":
        c["summary"] = ""
    return c


def rank(cv, jsnap, jobs):
    cs = cv_to_snapshot(cv, MODEL)
    scored = [(job["id"], compute_composite(cs, jsnap[job["id"]]).final_score) for job in jobs]
    scored.sort(key=lambda x: -x[1])
    return scored


def main() -> None:
    rng = np.random.default_rng(SEED)
    settings = Settings()
    cvs, jobs = load_settings_data(settings)
    jsnap = {job["id"]: job_to_snapshot(job, MODEL) for job in jobs}
    catalog = sorted({s for j in jobs for s in j.get("required_skills", [])} |
                     {s for c in cvs for s in c.get("skills", [])})

    baseline = {cv["id"]: rank(cv, jsnap, jobs) for cv in cvs}

    kinds = ["synonym_substitution", "capitalization", "formatting_noise", "missing_compensation",
             "missing_remote", "irrelevant_skill_insertion", "keyword_stuffing", "misspelling",
             "skill_deletion", "sparse_resume", "summary_removal"]
    expectation = {"synonym_substitution": "invariant", "capitalization": "invariant",
                   "formatting_noise": "invariant", "missing_compensation": "small",
                   "missing_remote": "small", "irrelevant_skill_insertion": "robust (small +)",
                   "keyword_stuffing": "robust (bounded +)", "misspelling": "small",
                   "skill_deletion": "sensitive (-)", "sparse_resume": "sensitive (-)",
                   "summary_removal": "sensitive (-)"}

    matrix = {}
    for kind in kinds:
        dcomp, stable, jac, signed = [], [], [], []
        for cv in cvs:
            base = baseline[cv["id"]]
            base_top, base_top_score = base[0]
            base_top5 = {d for d, _ in base[:5]}
            pr = rank(perturb(cv, kind, np.random.default_rng(SEED + _stable_offset(cv["id"])), catalog), jsnap, jobs)
            pr_top, pr_top_score = pr[0]
            pr_top5 = {d for d, _ in pr[:5]}
            # Δ composite on the ORIGINAL top job
            base_score_for_orig = dict(base)[base_top]
            pr_score_for_orig = dict(pr)[base_top]
            dcomp.append(abs(pr_score_for_orig - base_score_for_orig))
            signed.append(pr_score_for_orig - base_score_for_orig)
            stable.append(1 if pr_top == base_top else 0)
            jac.append(len(base_top5 & pr_top5) / len(base_top5 | pr_top5))
        matrix[kind] = {
            "expectation": expectation[kind],
            "mean_abs_delta_composite": round(float(np.mean(dcomp)), 4),
            "mean_signed_delta_composite": round(float(np.mean(signed)), 4),
            "top1_stability": round(float(np.mean(stable)), 4),
            "mean_top5_jaccard": round(float(np.mean(jac)), 4),
        }

    out = {
        "experiment": "EXP-029 robustness matrix (Stage-2 §R)",
        "n_resumes": len(cvs), "n_jobs": len(jobs), "seed": SEED,
        "matrix": matrix,
        "interpretation": (
            "Report per-perturbation Δcomposite / top-1 stability / top-5 Jaccard vs the expected behavior. "
            "Invariance types (synonym/caps/formatting) should show ~0 Δ and ~1.0 stability; injection/stuffing "
            "should show only a bounded score change (not a large jump); deletion/sparsity should reduce fit. "
            "Deviations are reported honestly (e.g., misspellings do perturb the composite; see EXP-007)."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
