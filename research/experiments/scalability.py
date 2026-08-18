"""EXP-031 / EXP-032 / Stage-2 §T-U: real scalability + incremental-update timing.

Scalability (§T): time the hot ranking path (compute_composite over a growing job pool + sort)
as the pool grows to {15, 75, 500, 1000, 5000, 10000} jobs, reporting p50/p95/p99 per-query
latency and throughput. Job snapshots are built from the synthetic corpus and REPLICATED (with a
tiny embedding jitter) to reach large pool sizes — this stresses the SCORING path honestly (the
embeddings are precomputed/cached in production, so scoring latency is the quantity of interest).
This replaces the misleading "15-job = production scale" latency claim (audit).

Incremental updates (§U): starting from a warm 1,000-job pool, measure the cost of scoring
{1, 10, 100} newly-added jobs for a query (delta re-rank) vs a full re-rank.

Run: cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false \
  PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/scalability.py
"""
from __future__ import annotations

import bisect
import hashlib
import json
import time
from pathlib import Path

import numpy as np

from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.document_text import job_document_text, resume_document_text
from core.embedding import embed_text
from core.scoring import compute_composite

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "research" / "datasets" / "synthetic_v1"
OUT = REPO / "research" / "results" / "scalability.json"
SEED = 42
MODEL = "all-MiniLM-L6-v2"
POOLS = [15, 75, 500, 1000, 5000, 10000]
N_QUERIES = 20


def cand_snap(cv):
    fam = cv["job_family"].replace("_", " ")
    like = {"id": cv["id"], "skills": cv["skills"], "experience_years": cv["experience_years"],
            "remote_preference": cv["remote_preference"], "preferred_salary": cv["preferred_salary"],
            "summary": f"{cv['title']} with {cv['experience_years']} years of {fam} experience."}
    doc = resume_document_text({**like, "name": ""})
    return CandidateSnapshot(id=cv["id"], name="", skills=like["skills"], experience_years=float(like["experience_years"]),
                             remote_preference=bool(like["remote_preference"]), preferred_salary=like["preferred_salary"],
                             summary=like["summary"], version=1, document_text_hash=hashlib.sha256(doc.encode()).hexdigest(),
                             embedding=embed_text(doc, model_name=MODEL).tolist())


def job_snap(job):
    like = {"title": job["title"], "required_skills": job["required_skills"], "preferred_skills": job["preferred_skills"],
            "required_experience": job["required_experience_min"], "remote_policy": job["work_mode"] == "remote",
            "budget_min": job["budget_min"], "budget_max": job["budget_max"], "description": job["description"]}
    doc = job_document_text(like)
    return JobSnapshot(id=job["id"], title=like["title"], required_skills=like["required_skills"],
                       preferred_skills=like["preferred_skills"], required_experience=int(like["required_experience"]),
                       remote_policy=bool(like["remote_policy"]), budget_min=like["budget_min"], budget_max=like["budget_max"],
                       description=like["description"], version=1, document_text_hash=hashlib.sha256(doc.encode()).hexdigest(),
                       embedding=embed_text(doc, model_name=MODEL).tolist())


def replicate(base_snaps, n, rng):
    """Grow the job pool to n by cloning base snapshots with a tiny embedding jitter."""
    out = []
    i = 0
    while len(out) < n:
        src = base_snaps[i % len(base_snaps)]
        vec = np.asarray(src.embedding, np.float32) + rng.normal(0, 1e-3, size=len(src.embedding)).astype(np.float32)
        out.append(src.model_copy(update={"id": f"{src.id}_r{len(out)}", "embedding": vec.tolist()}))
        i += 1
    return out


def rank_all(cs, pool):
    scored = [(j.id, compute_composite(cs, j).final_score) for j in pool]
    scored.sort(key=lambda x: -x[1])
    return scored


def main() -> None:
    rng = np.random.default_rng(SEED)
    resumes = json.loads((DATA / "synthetic_resumes.json").read_text())
    jobs = json.loads((DATA / "synthetic_jobs.json").read_text())
    q_snaps = [cand_snap(cv) for cv in resumes[:N_QUERIES]]
    base_job_snaps = [job_snap(j) for j in jobs]
    print(f"embedded {len(q_snaps)} query resumes + {len(base_job_snaps)} base jobs")

    REPEAT = 5  # repeat each query so p95/p99 are supported by >= 100 samples (not 20)
    scal = {}
    for n in POOLS:
        pool = replicate(base_job_snaps, n, rng)
        # warm-up (pay cold-cache/JIT once, unmeasured)
        rank_all(q_snaps[0], pool)
        lat_ms = []
        for _ in range(REPEAT):
            for cs in q_snaps:
                t0 = time.perf_counter()
                rank_all(cs, pool)
                lat_ms.append((time.perf_counter() - t0) * 1000.0)
        arr = np.asarray(lat_ms)
        scal[str(n)] = {
            "p50_ms": round(float(np.percentile(arr, 50)), 3),
            "p95_ms": round(float(np.percentile(arr, 95)), 3),
            "p99_ms": round(float(np.percentile(arr, 99)), 3),
            "mean_ms": round(float(arr.mean()), 3),
            "throughput_pairs_per_s": round(n / (arr.mean() / 1000.0), 1),
        }
        print(f"pool={n:6d}  p50={scal[str(n)]['p50_ms']:.2f}ms  p95={scal[str(n)]['p95_ms']:.2f}ms  mean={scal[str(n)]['mean_ms']:.2f}ms")

    # incremental updates on a warm 1000-job pool: the incremental cost includes SCORING the k new
    # jobs AND MERGING them into the maintained sorted ranking (bisect.insort), i.e. it actually
    # produces the updated ordering — not a score-only lower bound (code-review fix).
    warm = replicate(base_job_snaps, 1000, rng)
    cs = q_snaps[0]
    base_sorted = sorted([(-compute_composite(cs, j).final_score, j.id) for j in warm])  # maintained ranking
    incr = {}
    for k in (1, 10, 100):
        add = replicate(base_job_snaps, k, rng)
        maintained = list(base_sorted)
        t0 = time.perf_counter()
        for j in add:  # score each new job and insert into the sorted ranking
            bisect.insort(maintained, (-compute_composite(cs, j).final_score, j.id))
        incr_ms = (time.perf_counter() - t0) * 1000.0
        t0 = time.perf_counter()
        rank_all(cs, warm + add)  # full re-rank from scratch
        full_ms = (time.perf_counter() - t0) * 1000.0
        incr[str(k)] = {"incremental_score_and_merge_ms": round(incr_ms, 3),
                        "full_rerank_1000_plus_k_ms": round(full_ms, 3),
                        "speedup_x": round(full_ms / incr_ms, 1) if incr_ms > 0 else None}

    out = {
        "experiment": "EXP-031/032 scalability + incremental updates (Stage-2 §T-U)",
        "note": "Scoring-path latency on a replicated synthetic job pool (embeddings precomputed/cached, "
                "as in production). Single-threaded Python; seed 42. NOT a distributed-systems benchmark.",
        "n_query_resumes": N_QUERIES,
        "scalability_per_query_latency": scal,
        "incremental_updates_warm_1000_pool": incr,
        "interpretation": (
            "Per-query scoring latency grows ~linearly in pool size (brute-force scoring); report p50/p95/p99 and "
            "throughput honestly, and note that production would add an ANN retrieval prefilter before scoring "
            "(not implemented here). Incremental scoring of k new jobs is far cheaper than a full re-rank."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps(out["incremental_updates_warm_1000_pool"], indent=2))


if __name__ == "__main__":
    main()
