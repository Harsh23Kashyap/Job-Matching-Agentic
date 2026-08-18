"""EXP-024 / Stage-2 §F-H: STRUCTURE-RECOVERY test on the synthetic corpus.

Does the composite ranker RECOVER the KNOWN latent structure baked into the synthetic
corpus (EXP-023)? Because the synthetic ground truth is a TRANSPARENT latent-compatibility
function with stored per-factor values, we can test recovery directly — something impossible
on the small human corpus. This is a controlled *validity* probe, NOT a headline nDCG claim
(Stage-2 §F-H: "Do NOT use synthetic data to manufacture a favorable headline nDCG claim.").

Reported:
  1. Ranking recovery — per-resume nDCG@5 / nDCG@10 of the composite ranking vs the graded
     (clean) latent grades, mean + bootstrap CI. Compared against a random baseline and the
     oracle (rank by latent_score). Recovery = (composite - random) / (oracle - random).
  2. Global monotonicity — Spearman(composite_final, latent_score) over all pairs.
  3. Decomposition validity — Spearman(channel_score, its intended latent factor) for each of
     the six channels. This is the KEY explainability result: does each auditable channel
     recover the latent factor it is supposed to represent?
  4. Recovery by difficulty (easy/moderate/hard/adversarial) — does it degrade on hard cases?
  5. Noise robustness — nDCG vs clean grades AND vs the 8%-noisy labels (should be close).

Deterministic (seed 42). Run single-threaded to avoid the torch startup hang under load:
  OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false \
    PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/synthetic/structure_recovery.py
(from backend/). Env SR_SMOKE=1 embeds only 5 resumes/5 jobs as a fast hang check.
"""
from __future__ import annotations

import hashlib
import json
import os
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
OUT = REPO / "research" / "results" / "structure_recovery.json"
SEED = 42
MODEL = "all-MiniLM-L6-v2"

# channel -> the latent factor it is designed to recover (decomposition-validity mapping)
CHANNEL_FACTOR = {
    "skills": "required",
    "experience": "experience",
    "compensation": "comp",
    "remote": "workmode",
    "title": "family",
    "semantic": "__latent__",  # holistic; correlate against the full latent score
}


def _spearman(x, y):
    """Spearman rho via Pearson on ranks (numpy-only; avoids a scipy hard dep)."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if len(x) < 3 or np.all(x == x[0]) or np.all(y == y[0]):
        return None
    rx = _rankdata(x)
    ry = _rankdata(y)
    return float(np.corrcoef(rx, ry)[0, 1])


def _rankdata(a):
    a = np.asarray(a, float)
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), float)
    ranks[order] = np.arange(1, len(a) + 1)
    # average tied ranks
    _, inv, counts = np.unique(a, return_inverse=True, return_counts=True)
    csum = np.cumsum(counts)
    start = csum - counts
    avg = (start + csum - 1) / 2.0 + 1.0
    return avg[inv]


def _cv_like(cv: dict) -> dict:
    """Map a synthetic resume onto the field names the production doc-text/snapshot expect."""
    fam = cv["job_family"].replace("_", " ")
    return {
        "id": cv["id"],
        "name": "",
        "skills": cv["skills"],
        "experience_years": cv["experience_years"],
        "remote_preference": cv["remote_preference"],
        "preferred_salary": cv["preferred_salary"],
        "summary": f"{cv['title']} with {cv['experience_years']} years of {fam} experience.",
    }


def _job_like(job: dict) -> dict:
    return {
        "id": job["id"],
        "title": job["title"],
        "required_skills": job["required_skills"],
        "preferred_skills": job["preferred_skills"],
        "required_experience": job["required_experience_min"],
        "remote_policy": job["work_mode"] == "remote",
        "budget_min": job["budget_min"],
        "budget_max": job["budget_max"],
        "description": job["description"],
    }


def _cand_snapshot(cv: dict) -> CandidateSnapshot:
    like = _cv_like(cv)
    doc = resume_document_text(like)
    return CandidateSnapshot(
        id=like["id"], name="", skills=like["skills"],
        experience_years=float(like["experience_years"]),
        remote_preference=bool(like["remote_preference"]),
        preferred_salary=like["preferred_salary"], summary=like["summary"],
        version=1, document_text_hash=hashlib.sha256(doc.encode()).hexdigest(),
        embedding=embed_text(doc, model_name=MODEL).tolist(),
    )


def _job_snapshot(job: dict) -> JobSnapshot:
    like = _job_like(job)
    doc = job_document_text(like)
    return JobSnapshot(
        id=like["id"], title=like["title"], required_skills=like["required_skills"],
        preferred_skills=like["preferred_skills"], required_experience=int(like["required_experience"]),
        remote_policy=bool(like["remote_policy"]), budget_min=like["budget_min"],
        budget_max=like["budget_max"], description=like["description"], version=1,
        document_text_hash=hashlib.sha256(doc.encode()).hexdigest(),
        embedding=embed_text(doc, model_name=MODEL).tolist(),
    )


def _bootstrap_ci(vals, n_boot=2000, seed=SEED):
    rng = np.random.default_rng(seed)
    arr = np.asarray(vals, float)
    if len(arr) == 0:
        return {"mean": None, "ci_low": None, "ci_high": None}
    boots = np.array([arr[rng.integers(0, len(arr), len(arr))].mean() for _ in range(n_boot)])
    return {"mean": round(float(arr.mean()), 6),
            "ci_low": round(float(np.quantile(boots, 0.025)), 6),
            "ci_high": round(float(np.quantile(boots, 0.975)), 6)}


def main() -> None:
    np.random.seed(SEED)
    smoke = os.getenv("SR_SMOKE", "").strip() in ("1", "true", "yes")

    resumes = json.loads((DATA / "synthetic_resumes.json").read_text())
    jobs = json.loads((DATA / "synthetic_jobs.json").read_text())
    rel_payload = json.loads((DATA / "synthetic_relevance.json").read_text())
    labels = rel_payload["labels"]

    if smoke:
        resumes, jobs = resumes[:5], jobs[:5]
        keep_c = {r["id"] for r in resumes}
        keep_j = {j["id"] for j in jobs}
        labels = [l for l in labels if l["query_id"] in keep_c and l["doc_id"] in keep_j]

    # index labels: (qid, doc_id) -> label row
    lab = {(l["query_id"], l["doc_id"]): l for l in labels}

    # embed once
    cand_snaps = {r["id"]: _cand_snapshot(r) for r in resumes}
    job_snaps = {j["id"]: _job_snapshot(j) for j in jobs}
    print(f"embedded {len(cand_snaps)} resumes + {len(job_snaps)} jobs")

    # score every pair
    rng = np.random.default_rng(SEED)
    ndcg5_comp, ndcg10_comp, ndcg5_rand, ndcg5_oracle = [], [], [], []
    ndcg5_noisy = []
    by_diff = defaultdict(list)  # difficulty -> [nDCG@5]
    global_comp, global_latent = [], []
    chan_series = defaultdict(list)   # channel -> [channel_score]
    factor_series = defaultdict(list)  # factor  -> [latent_factor value]
    diff_of = {r["id"]: r["difficulty"] for r in resumes}

    for cv in resumes:
        cid = cv["id"]
        rows = []  # (job_id, composite, clean_grade, noisy_grade, latent, channels, factors)
        for job in jobs:
            jid = job["id"]
            key = (cid, jid)
            if key not in lab:
                continue
            l = lab[key]
            bd = compute_composite(cand_snaps[cid], job_snaps[jid])
            ch = {"semantic": bd.semantic_score, "skills": bd.skills_score, "title": bd.title_score,
                  "experience": bd.experience_score, "compensation": bd.compensation_score,
                  "remote": bd.remote_score}
            rows.append((jid, bd.final_score, l["clean_grade"], l["relevance"],
                         l["latent_score"], ch, l["latent_factors"]))

        if not rows:
            continue
        # graded relevance maps
        relmap_clean = {r[0]: r[2] for r in rows}
        relmap_noisy = {r[0]: r[3] for r in rows}
        if not any(v > 0 for v in relmap_clean.values()):
            continue

        comp_rank = [r[0] for r in sorted(rows, key=lambda r: -r[1])]
        oracle_rank = [r[0] for r in sorted(rows, key=lambda r: -r[4])]
        rand_rank = list(comp_rank)
        rng.shuffle(rand_rank)

        n5 = ndcg_at_k(comp_rank, relmap_clean, 5)
        ndcg5_comp.append(n5)
        ndcg10_comp.append(ndcg_at_k(comp_rank, relmap_clean, 10))
        ndcg5_rand.append(ndcg_at_k(rand_rank, relmap_clean, 5))
        ndcg5_oracle.append(ndcg_at_k(oracle_rank, relmap_clean, 5))
        ndcg5_noisy.append(ndcg_at_k(comp_rank, relmap_noisy, 5))
        by_diff[diff_of[cid]].append(n5)

        for r in rows:
            global_comp.append(r[1])
            global_latent.append(r[4])
            for chan, factor in CHANNEL_FACTOR.items():
                chan_series[chan].append(r[5][chan])
                factor_series[chan].append(r[4] if factor == "__latent__" else r[6][factor])

    comp_ci = _bootstrap_ci(ndcg5_comp)
    rand_mean = round(float(np.mean(ndcg5_rand)), 6)
    oracle_mean = round(float(np.mean(ndcg5_oracle)), 6)
    recovery = None
    if oracle_mean - rand_mean > 1e-9:
        recovery = round((comp_ci["mean"] - rand_mean) / (oracle_mean - rand_mean), 4)

    decomposition = {}
    for chan in CHANNEL_FACTOR:
        decomposition[chan] = {
            "recovers_factor": CHANNEL_FACTOR[chan],
            "spearman": round(_spearman(chan_series[chan], factor_series[chan]), 4)
            if _spearman(chan_series[chan], factor_series[chan]) is not None else None,
        }

    out = {
        "experiment": "EXP-024 structure recovery on synthetic_v1 (Stage-2 §F-H)",
        "provenance": "SYNTHETIC / CONTROLLED — validity probe, NOT a human-benchmark headline number",
        "seed": SEED, "smoke": smoke,
        "n_resumes": len(resumes), "n_jobs": len(jobs),
        "ranking_recovery": {
            "composite_ndcg@5": comp_ci,
            "composite_ndcg@10_mean": round(float(np.mean(ndcg10_comp)), 6),
            "random_baseline_ndcg@5": rand_mean,
            "oracle_ndcg@5": oracle_mean,
            "recovery_ratio": recovery,
            "recovery_ratio_note": "(composite - random) / (oracle - random); 1.0 = perfect recovery, 0 = random",
        },
        "noise_robustness": {
            "composite_ndcg@5_vs_clean": comp_ci["mean"],
            "composite_ndcg@5_vs_8pct_noisy": round(float(np.mean(ndcg5_noisy)), 6),
        },
        "global_monotonicity": {
            "spearman_composite_vs_latent": round(_spearman(global_comp, global_latent), 4)
            if _spearman(global_comp, global_latent) is not None else None,
            "n_pairs": len(global_comp),
        },
        "decomposition_validity": decomposition,
        "recovery_by_difficulty": {d: round(float(np.mean(v)), 4) for d, v in sorted(by_diff.items())},
        "interpretation": (
            "High composite-vs-oracle recovery + strong per-channel Spearman => the auditable "
            "decomposition recovers the KNOWN latent structure, supporting the explainability claim "
            "on controlled data. Report as a synthetic VALIDITY result, never as a human-benchmark nDCG."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
