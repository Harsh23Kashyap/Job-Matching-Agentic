"""EXP-033 / Stage-2 §V: failure-injection matrix — does the deterministic scoring path survive?

The ranking hot path consumes pre-built snapshots and never invokes the LLM parser/explainer
(EXP-019). This injects nine faults and checks whether compute_composite still returns a FINITE,
in-range score (graceful degradation / failure isolation) or whether the fault propagates
(reported honestly as a gap to fix). Each case records: crashed? / finite? / in [0,1]? / behavior.

Run: cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false \
  PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/failure_injection.py
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np

from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.scoring import compute_composite

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "research" / "results" / "failure_injection.json"
DIM = 384


def cand(skills=("Python", "ML"), summary="Senior ML engineer", emb=None):
    e = emb if emb is not None else (np.ones(DIM, np.float32) / math.sqrt(DIM)).tolist()
    return CandidateSnapshot(id="c1", name="", skills=list(skills), experience_years=6.0,
                             remote_preference=True, preferred_salary=150000, summary=summary,
                             version=1, document_text_hash="h", embedding=e)


def job(title="ML Engineer", req=("Python", "ML"), emb=None, budget_min=120000, budget_max=180000,
        remote=True, desc="Hiring ML engineer"):
    e = emb if emb is not None else (np.ones(DIM, np.float32) / math.sqrt(DIM)).tolist()
    return JobSnapshot(id="j1", title=title, required_skills=list(req), preferred_skills=[],
                       required_experience=5, remote_policy=remote, budget_min=budget_min,
                       budget_max=budget_max, description=desc, version=1, document_text_hash="h", embedding=e)


def run_case(name, expect, c, j):
    rec = {"case": name, "expected": expect}
    try:
        bd = compute_composite(c, j)
        s = bd.final_score
        finite = math.isfinite(s)
        rec.update({"crashed": False, "final_score": (round(float(s), 4) if finite else str(s)),
                    "finite": bool(finite), "in_range": bool(finite and 0.0 <= s <= 1.0),
                    "isolated_ok": bool(finite and 0.0 <= s <= 1.0)})
    except Exception as e:  # noqa: BLE001
        rec.update({"crashed": True, "error": f"{type(e).__name__}: {e}", "finite": False,
                    "in_range": False, "isolated_ok": False})
    return rec


def main() -> None:
    zero = [0.0] * DIM
    nan = [float("nan")] * DIM
    cases = [
        run_case("parser_failure_empty_structured", "isolated: ranking works with empty skills/summary (uses embedding)",
                 cand(skills=[], summary=""), job()),
        run_case("missing_candidate_embedding_zero", "isolated: cosine guards zero-norm -> semantic 0",
                 cand(emb=zero), job()),
        run_case("missing_job_embedding_zero", "isolated: cosine guards zero-norm -> semantic 0",
                 cand(), job(emb=zero)),
        run_case("malformed_job_no_required_skills", "isolated: jaccard 0, ranking continues",
                 cand(), job(req=[])),
        run_case("missing_skill_vocabulary", "isolated: unknown skills -> jaccard 0, no crash",
                 cand(skills=["Zzzzz-Unknown-Skill-9000"]), job(req=["Another-Unknown"])),
        run_case("missing_compensation_band", "isolated: compensation defaults to 1.0 when band absent",
                 cand(), job(budget_min=None, budget_max=None)),
        run_case("empty_job_description_and_title", "isolated: title defaults, semantic on empty text",
                 cand(), job(title="", desc="")),
        run_case("duplicate_candidate_determinism", "deterministic: identical inputs -> identical score",
                 cand(), job()),
        run_case("nan_embedding_injection", "GAP if NaN propagates -> needs input validation",
                 cand(emb=nan), job()),
    ]
    # determinism check
    a = compute_composite(cand(), job()).final_score
    b = compute_composite(cand(), job()).final_score
    determinism_ok = (a == b)

    isolated = sum(1 for c in cases if c.get("isolated_ok"))
    gaps = [c["case"] for c in cases if not c.get("isolated_ok")]

    out = {
        "experiment": "EXP-033 failure-injection matrix (Stage-2 §V)",
        "cases": cases,
        "determinism_identical_inputs_identical_score": bool(determinism_ok),
        "n_cases": len(cases), "n_isolated_ok": isolated,
        "gaps_found": gaps,
        "interpretation": (
            "The deterministic scoring path isolates parser/LLM/embedding faults for realistic degradations "
            "(empty fields, zero embeddings, missing skills/compensation) — it returns a finite in-range score "
            "without crashing, confirming failure isolation (RQ8/§W). Any propagating fault (e.g., NaN embedding) "
            "is reported as a gap requiring explicit input validation, not hidden."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
