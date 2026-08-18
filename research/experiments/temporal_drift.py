"""EXP-030 / Stage-2 §S: temporal-drift CONTROLLED SIMULATION (not real temporal data).

We have no real timestamps, so this is explicitly a SIMULATION (Stage-2 §S: "Don't claim real
temporal validation if simulated."). On the synthetic corpus we simulate three drift regimes on
the JOB side and measure composite nDCG@5 degradation vs the no-drift baseline:
  emerging_skills : a fraction of required skills are renamed to unseen 'NextGen-' variants that
                    do not lexically match the resume skill vocabulary (new technologies).
  changed_titles  : job titles are rewritten to novel phrasings (role-name drift).
  salary_shift    : budgets inflated (+30%) so compensation bands drift.
Baseline = the composite ranking on the un-drifted jobs vs the same latent grades.

Run: cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false \
  PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/temporal_drift.py
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import numpy as np

from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.document_text import job_document_text, resume_document_text
from core.embedding import embed_text
from core.scoring import compute_composite
from benchmarks.metrics import ndcg_at_k

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "research" / "datasets" / "synthetic_v1"
OUT = REPO / "research" / "results" / "temporal_drift.json"
SEED = 42
MODEL = "all-MiniLM-L6-v2"


def cand_snap(cv):
    fam = cv["job_family"].replace("_", " ")
    like = {"id": cv["id"], "name": "", "skills": cv["skills"], "experience_years": cv["experience_years"],
            "remote_preference": cv["remote_preference"], "preferred_salary": cv["preferred_salary"],
            "summary": f"{cv['title']} with {cv['experience_years']} years of {fam} experience."}
    doc = resume_document_text(like)
    return CandidateSnapshot(id=like["id"], name="", skills=like["skills"], experience_years=float(like["experience_years"]),
                             remote_preference=bool(like["remote_preference"]), preferred_salary=like["preferred_salary"],
                             summary=like["summary"], version=1, document_text_hash=hashlib.sha256(doc.encode()).hexdigest(),
                             embedding=embed_text(doc, model_name=MODEL).tolist())


def job_snap(job):
    like = {"id": job["id"], "title": job["title"], "required_skills": job["required_skills"],
            "preferred_skills": job["preferred_skills"], "required_experience": job["required_experience_min"],
            "remote_policy": job["work_mode"] == "remote", "budget_min": job["budget_min"],
            "budget_max": job["budget_max"], "description": job["description"]}
    doc = job_document_text(like)
    return JobSnapshot(id=like["id"], title=like["title"], required_skills=like["required_skills"],
                       preferred_skills=like["preferred_skills"], required_experience=int(like["required_experience"]),
                       remote_policy=bool(like["remote_policy"]), budget_min=like["budget_min"], budget_max=like["budget_max"],
                       description=like["description"], version=1, document_text_hash=hashlib.sha256(doc.encode()).hexdigest(),
                       embedding=embed_text(doc, model_name=MODEL).tolist())


def drift(job, kind, rng):
    j = copy.deepcopy(job)
    if kind == "emerging_skills":
        j["required_skills"] = [f"NextGen-{s}" for s in j["required_skills"]]
    elif kind == "changed_titles":
        j["title"] = f"{j['title']} Specialist (Cloud-Native, GenAI-era)"
        j["description"] = j["description"] + " Modern reimagined role."
    elif kind == "salary_shift":
        j["budget_min"] = int(j["budget_min"] * 1.3)
        j["budget_max"] = int(j["budget_max"] * 1.3)
    return j


def eval_ndcg(resumes, job_snaps_by_id, jobs, lab, subset_ids):
    per = []
    for cv in resumes:
        cs = cand_snap(cv)
        rows = []
        for job in jobs:
            key = (cv["id"], job["id"])
            if key not in lab:
                continue
            rows.append((job["id"], compute_composite(cs, job_snaps_by_id[job["id"]]).final_score, lab[key]["clean_grade"]))
        relmap = {r[0]: r[2] for r in rows}
        if not any(v > 0 for v in relmap.values()):
            continue
        ranking = [r[0] for r in sorted(rows, key=lambda x: -x[1])]
        per.append(ndcg_at_k(ranking, relmap, 5))
    return float(np.mean(per)) if per else None


def main() -> None:
    rng = np.random.default_rng(SEED)
    resumes = json.loads((DATA / "synthetic_resumes.json").read_text())[:120]
    jobs = json.loads((DATA / "synthetic_jobs.json").read_text())
    labels = json.loads((DATA / "synthetic_relevance.json").read_text())["labels"]
    keep_c = {r["id"] for r in resumes}
    lab = {(l["query_id"], l["doc_id"]): l for l in labels if l["query_id"] in keep_c}

    base_snaps = {j["id"]: job_snap(j) for j in jobs}
    base = eval_ndcg(resumes, base_snaps, jobs, lab, None)

    results = {"baseline_no_drift_ndcg@5": round(base, 4)}
    for kind in ("emerging_skills", "changed_titles", "salary_shift"):
        drifted = [drift(j, kind, rng) for j in jobs]
        dsnaps = {j["id"]: job_snap(j) for j in drifted}
        nd = eval_ndcg(resumes, dsnaps, jobs, lab, None)
        results[kind] = {"ndcg@5": round(nd, 4), "degradation": round(base - nd, 4),
                         "relative_pct": round(100 * (base - nd) / base, 2) if base else None}

    out = {
        "experiment": "EXP-030 temporal drift — CONTROLLED SIMULATION (Stage-2 §S)",
        "provenance": "SIMULATED drift on synthetic_v1 (no real timestamps); NOT real temporal validation",
        "n_resumes": len(resumes), "n_jobs": len(jobs), "seed": SEED,
        "results": results,
        "interpretation": (
            "Degradation under simulated drift quantifies sensitivity to emerging skills / renamed roles / "
            "salary shifts. Emerging-skill drift is expected to hurt most (skills channel loses lexical overlap; "
            "semantic partially compensates). Report explicitly as a SIMULATION and as a limitation (no real "
            "temporal data), never as real temporal validation."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
