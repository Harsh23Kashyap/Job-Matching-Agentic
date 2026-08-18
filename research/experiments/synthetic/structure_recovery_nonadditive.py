"""EXP-024b / Stage-3 (Opus-5 OBJ-2): structure recovery under a NON-ADDITIVE latent generator.

Objection: EXP-024's 90.7% recovery is partly true BY CONSTRUCTION because the synthetic latent is an
ADDITIVE blend of factors aligned with the composite's additive channels. This probe re-grades the SAME
synthetic corpus with a NON-ADDITIVE latent that does NOT mirror the composite's functional form, then
measures whether the additive composite still recovers it. If recovery collapses -> the additive composite
is limited under interaction structure (honest limitation). If it holds -> the composite is robust to
functional-form mismatch (a real, non-trivial result). Either way it de-risks the by-construction critique.

Non-additive latent (multiplicative / hard-conjunctive, using the SAME stored latent_factors):
    latent_mult = required^0.5 * seniority^0.2 * experience^0.2 * family^0.1   (geometric; a hard gate:
    if required==0 the pair is a non-match regardless of other factors — decidedly NOT additive).
Grades are re-thresholded by QUANTILES to reproduce the ADDITIVE grade-distribution proportions, so label
balance/difficulty is held constant and only the STRUCTURE (additive vs multiplicative) differs.

Run: cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false \
  PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/synthetic/structure_recovery_nonadditive.py
"""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.document_text import job_document_text, resume_document_text
from core.embedding import embed_text
from core.scoring import compute_composite
from benchmarks.metrics import ndcg_at_k

REPO = Path(__file__).resolve().parents[3]
DATA = REPO / "research" / "datasets" / "synthetic_v1"
OUT = REPO / "research" / "results" / "structure_recovery_nonadditive.json"
SEED = 42
MODEL = "all-MiniLM-L6-v2"
ADDITIVE_BASELINE = 0.9066  # EXP-024 recovery ratio (additive latent)


def _cand(cv):
    fam = cv["job_family"].replace("_", " ")
    like = {"id": cv["id"], "skills": cv["skills"], "experience_years": cv["experience_years"],
            "remote_preference": cv["remote_preference"], "preferred_salary": cv["preferred_salary"],
            "summary": f"{cv['title']} with {cv['experience_years']} years of {fam} experience."}
    doc = resume_document_text({**like, "name": ""})
    return CandidateSnapshot(id=cv["id"], name="", skills=like["skills"], experience_years=float(like["experience_years"]),
                             remote_preference=bool(like["remote_preference"]), preferred_salary=like["preferred_salary"],
                             summary=like["summary"], version=1, document_text_hash=hashlib.sha256(doc.encode()).hexdigest(),
                             embedding=embed_text(doc, model_name=MODEL).tolist())


def _job(job):
    like = {"title": job["title"], "required_skills": job["required_skills"], "preferred_skills": job["preferred_skills"],
            "required_experience": job["required_experience_min"], "remote_policy": job["work_mode"] == "remote",
            "budget_min": job["budget_min"], "budget_max": job["budget_max"], "description": job["description"]}
    doc = job_document_text(like)
    return JobSnapshot(id=job["id"], title=like["title"], required_skills=like["required_skills"],
                       preferred_skills=like["preferred_skills"], required_experience=int(like["required_experience"]),
                       remote_policy=bool(like["remote_policy"]), budget_min=like["budget_min"], budget_max=like["budget_max"],
                       description=like["description"], version=1, document_text_hash=hashlib.sha256(doc.encode()).hexdigest(),
                       embedding=embed_text(doc, model_name=MODEL).tolist())


def nonadditive_latent(f):
    r = max(f["required"], 0.0)
    if r <= 0.0:
        return 0.0  # hard gate: no required-skill satisfaction => non-match (non-additive)
    return (r ** 0.5) * (max(f["seniority"], 0.01) ** 0.2) * (max(f["experience"], 0.01) ** 0.2) * (max(f["family"], 0.01) ** 0.1)


def _bootstrap_ci(vals, n_boot=2000, seed=SEED):
    rng = np.random.default_rng(seed); arr = np.asarray(vals, float)
    boots = np.array([arr[rng.integers(0, len(arr), len(arr))].mean() for _ in range(n_boot)])
    return {"mean": round(float(arr.mean()), 6), "ci_low": round(float(np.quantile(boots, 0.025)), 6),
            "ci_high": round(float(np.quantile(boots, 0.975)), 6)}


def main() -> None:
    resumes = json.loads((DATA / "synthetic_resumes.json").read_text())
    jobs = json.loads((DATA / "synthetic_jobs.json").read_text())
    labels = json.loads((DATA / "synthetic_relevance.json").read_text())["labels"]
    lab = {(l["query_id"], l["doc_id"]): l for l in labels}

    # recompute non-additive latent from the STORED factors; re-threshold by quantiles to match
    # the additive grade proportions (grade dist 0:27832 1:6427 2:2002 3:1239 over 37500)
    nd_lat = {(l["query_id"], l["doc_id"]): nonadditive_latent(l["latent_factors"]) for l in labels}
    vals = np.array(sorted(nd_lat.values()))
    # additive grade proportions
    add_grades = [l["clean_grade"] for l in labels]
    from collections import Counter
    c = Counter(add_grades); n = len(add_grades)
    p0 = c[0]/n; p1 = c[1]/n; p2 = c[2]/n  # p3 = remainder
    q1 = np.quantile(vals, p0)              # below q1 -> grade 0
    q2 = np.quantile(vals, p0 + p1)         # -> grade 1
    q3 = np.quantile(vals, p0 + p1 + p2)    # -> grade 2 ; above -> grade 3

    def grade(v):
        return 3 if v >= q3 else 2 if v >= q2 else 1 if v >= q1 else 0
    na_grade = {k: grade(v) for k, v in nd_lat.items()}

    cand = {r["id"]: _cand(r) for r in resumes}
    jsn = {j["id"]: _job(j) for j in jobs}
    print(f"embedded {len(cand)} resumes + {len(jsn)} jobs")

    rng = np.random.default_rng(SEED)
    comp_nd, rand_nd, oracle_nd = [], [], []
    by_diff = defaultdict(list)
    diff_of = {r["id"]: r["difficulty"] for r in resumes}
    for cv in resumes:
        rows = []
        for job in jobs:
            key = (cv["id"], job["id"])
            if key not in lab:
                continue
            bd = compute_composite(cand[cv["id"]], jsn[job["id"]])
            rows.append((job["id"], bd.final_score, na_grade[key], nd_lat[key]))
        relmap = {r[0]: r[2] for r in rows}
        if not any(v > 0 for v in relmap.values()):
            continue
        comp_rank = [r[0] for r in sorted(rows, key=lambda r: -r[1])]
        oracle_rank = [r[0] for r in sorted(rows, key=lambda r: -r[3])]
        rand_rank = list(comp_rank); rng.shuffle(rand_rank)
        n5 = ndcg_at_k(comp_rank, relmap, 5)
        comp_nd.append(n5)
        oracle_nd.append(ndcg_at_k(oracle_rank, relmap, 5))
        rand_nd.append(ndcg_at_k(rand_rank, relmap, 5))
        by_diff[diff_of[cv["id"]]].append(n5)

    ci = _bootstrap_ci(comp_nd)
    rand_m = round(float(np.mean(rand_nd)), 6); oracle_m = round(float(np.mean(oracle_nd)), 6)
    recovery = round((ci["mean"] - rand_m) / (oracle_m - rand_m), 4) if oracle_m - rand_m > 1e-9 else None

    out = {
        "experiment": "EXP-024b non-additive-latent structure recovery (Stage-3; addresses by-construction objection)",
        "latent_form": "multiplicative/hard-gated: required^0.5 * seniority^0.2 * experience^0.2 * family^0.1 (NOT additive; NOT the composite's form)",
        "grades": "re-thresholded by quantiles to match the additive grade proportions (label balance held constant)",
        "composite_ndcg@5_vs_nonadditive": ci,
        "random_baseline_ndcg@5": rand_m, "oracle_ndcg@5": oracle_m,
        "recovery_ratio_nonadditive": recovery,
        "recovery_ratio_additive_baseline_EXP024": ADDITIVE_BASELINE,
        "delta_vs_additive": round(recovery - ADDITIVE_BASELINE, 4) if recovery is not None else None,
        "recovery_by_difficulty": {d: round(float(np.mean(v)), 4) for d, v in sorted(by_diff.items())},
        "interpretation": (
            "If recovery_ratio_nonadditive is much lower than the additive baseline (0.907), the additive "
            "composite is genuinely limited under interaction/gated structure (honest limitation, refutes 'the "
            "synthetic is rigged for the composite'). If it stays comparable, the composite recovers even a "
            "non-additive ground truth, showing the additive recovery was NOT merely by construction."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps({k: out[k] for k in ("composite_ndcg@5_vs_nonadditive", "random_baseline_ndcg@5",
                                          "oracle_ndcg@5", "recovery_ratio_nonadditive",
                                          "recovery_ratio_additive_baseline_EXP024", "delta_vs_additive",
                                          "recovery_by_difficulty")}, indent=2))


if __name__ == "__main__":
    main()
