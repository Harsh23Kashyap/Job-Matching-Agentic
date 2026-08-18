"""Powered re-evaluation harness (Goal-2 enablement, per supervisor feedback 2026-08-18).

The moment the explicitly-negative-judged labels exist (annotate annotation_sheet_unjudged.csv ->
merge_annotations.py -> data/eval_pairs_expanded.json), this runs the powered re-test in ONE command:
label distribution (are there real negatives now?), per-method nDCG@5, the composite-vs-semantic
significance re-test (paired bootstrap CI + permutation p), and the jaccard/exact/graded skill-channel
decomposition — so we can see whether the ranking / relation-aware findings HOLD with real power.

Self-contained (does NOT modify the reproduce_all pipeline). Reuses the validated benchmark functions.
It reports whatever the data say; if the composite still doesn't beat semantic, that parity is the finding.

Eval file resolution (override with EVAL_PAIRS=/path or argv[1]):
  1) the given path, else 2) data/eval_pairs_expanded.json if it exists, else 3) data/eval_pairs.json.

Run: cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false PYTHONHASHSEED=0 \
  PYTHONPATH=. .venv/bin/python ../research/experiments/powered_reeval.py
"""
from __future__ import annotations

import os
import sys
import json
from pathlib import Path

import numpy as np

from config import Settings
from core.scoring import compute_composite, compute_semantic, COMPOSITE_WEIGHTS
from core.skills import jaccard_skills, graded_coverage_skills
from benchmarks.eval_data import load_eval_labels, cv_to_snapshot, job_to_snapshot
from benchmarks.extended_evaluation import load_settings_data
from benchmarks.metrics import ndcg_at_k

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "research" / "results" / "powered_reeval.json"
MODEL = "all-MiniLM-L6-v2"
SEED = 42


def _resolve_eval_path(settings) -> Path:
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    if os.environ.get("EVAL_PAIRS"):
        return Path(os.environ["EVAL_PAIRS"])
    expanded = settings.data_dir / "eval_pairs_expanded.json"
    return expanded if expanded.exists() else settings.data_dir / "eval_pairs.json"


def _bootstrap_perm(a: dict, b: dict, n_boot=3000, n_perm=20000, seed=SEED):
    common = sorted(set(a) & set(b))
    da = np.array([a[q] - b[q] for q in common])
    if len(da) == 0:
        return {"delta_mean": 0.0, "ci_low": 0.0, "ci_high": 0.0, "perm_p": 1.0, "n": 0}
    rng = np.random.default_rng(seed)
    boots = np.array([da[rng.integers(0, len(da), len(da))].mean() for _ in range(n_boot)])
    lo, hi = float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))
    prng = np.random.default_rng(seed + 7)
    signs = prng.integers(0, 2, size=(n_perm, len(da))) * 2 - 1
    perm_p = float((np.sum(np.abs((signs * da).mean(axis=1)) >= abs(da.mean())) + 1) / (n_perm + 1))
    return {"delta_mean": round(float(da.mean()), 5), "ci_low": round(lo, 5), "ci_high": round(hi, 5),
            "excludes_zero": bool(lo > 0 or hi < 0), "perm_p": round(perm_p, 4), "n": len(da)}


def main() -> None:
    settings = Settings()
    eval_path = _resolve_eval_path(settings)
    eval_map = load_eval_labels(eval_path)
    cvs, jobs = load_settings_data(settings)
    csnap = {cv["id"]: cv_to_snapshot(cv, MODEL) for cv in cvs}
    jsnap = {job["id"]: job_to_snapshot(job, MODEL) for job in jobs}
    cvmap = {cv["id"]: cv for cv in cvs}
    jobmap = {job["id"]: job for job in jobs}
    jids = [job["id"] for job in jobs]
    w = COMPOSITE_WEIGHTS

    # label distribution — the point of G2 is to see explicit negatives (grade 0) appear
    all_grades = [g for rel in eval_map.values() for g in rel.values()]
    dist = {g: sum(1 for x in all_grades if x == g) for g in sorted(set(all_grades))}
    n_neg = sum(1 for x in all_grades if x == 0)
    queries_with_neg = sum(1 for rel in eval_map.values() if any(v == 0 for v in rel.values()))

    # precompute non-skill channels once (composite is linear in the skill channel)
    chan, sem = {}, {}
    for cid in cvmap:
        for jid in jids:
            bd = compute_composite(csnap[cid], jsnap[jid], skills_mode="jaccard")
            chan[(cid, jid)] = {"semantic": bd.semantic_score or 0.0, "title": bd.title_score or 0.0,
                                "experience": bd.experience_score or 0.0, "compensation": bd.compensation_score or 0.0,
                                "remote": bd.remote_score or 0.0, "_jac": bd.skills_score or 0.0}
            sem[(cid, jid)] = bd.semantic_score or 0.0

    def _final(cid, jid, skill_val):
        c = chan[(cid, jid)]
        return max(0.0, min(1.0, w["semantic"] * c["semantic"] + w["title"] * c["title"]
                   + w["experience"] * c["experience"] + w["compensation"] * c["compensation"]
                   + w["remote"] * c["remote"] + w["skills"] * skill_val))

    def per_query(score_of):
        out = {}
        for cid in cvmap:
            relmap = eval_map.get(cid, {})
            if not any(v > 0 for v in relmap.values()):
                continue
            scores = {jid: score_of(cid, jid) for jid in jids}
            ranking = sorted(scores, key=lambda j: -scores[j])
            out[cid] = ndcg_at_k(ranking, relmap, 5)
        return out

    jac = lambda cid, jid: chan[(cid, jid)]["_jac"]
    grd = lambda credit: (lambda cid, jid: graded_coverage_skills(
        cvmap[cid].get("skills", []), jobmap[jid].get("required_skills", []), related_credit=credit))

    methods = {
        "composite_jaccard": per_query(lambda c, j: _final(c, j, jac(c, j))),
        "composite_graded_exact": per_query(lambda c, j: _final(c, j, grd(0.0)(c, j))),
        "composite_graded_related": per_query(lambda c, j: _final(c, j, grd(0.5)(c, j))),
        "semantic_only": per_query(lambda c, j: sem[(c, j)]),
    }
    ndcg = {k: round(float(np.mean(list(v.values()))), 5) for k, v in methods.items() if v}

    out = {
        "experiment": "Powered re-evaluation (Goal-2 enablement)",
        "eval_file": str(eval_path.relative_to(REPO)) if str(eval_path).startswith(str(REPO)) else str(eval_path),
        "n_labeled_pairs": len(all_grades),
        "grade_distribution": dist,
        "explicit_negatives_present": n_neg > 0,
        "n_explicit_negatives": n_neg,
        "queries_with_a_negative": queries_with_neg,
        "n_queries_scored": len(methods["composite_jaccard"]),
        "ndcg5_by_method": ndcg,
        "composite_vs_semantic": _bootstrap_perm(methods["composite_jaccard"], methods["semantic_only"]),
        "graded_vs_jaccard": _bootstrap_perm(methods["composite_graded_related"], methods["composite_jaccard"]),
        "relation_aware_vs_exact_coverage": _bootstrap_perm(methods["composite_graded_related"], methods["composite_graded_exact"]),
        "interpretation": (
            "If explicit_negatives_present is False, this is still the positive-only corpus and the re-test "
            "is NOT yet powered — annotate annotation_sheet_unjudged.csv and merge first. Once negatives are "
            "present, read composite_vs_semantic and the graded decomposition with the new power; report "
            "parity honestly if the composite still does not significantly beat semantic."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps({k: out[k] for k in ("eval_file", "n_labeled_pairs", "grade_distribution",
          "explicit_negatives_present", "n_explicit_negatives", "n_queries_scored", "ndcg5_by_method",
          "composite_vs_semantic", "graded_vs_jaccard", "relation_aware_vs_exact_coverage")}, indent=2))
    if not out["explicit_negatives_present"]:
        print("\nNOTE: no explicit negatives yet -> this is the positive-only baseline run (tooling smoke-test). "
              "Fill + merge the annotation sheet, then re-run for the POWERED test.")


if __name__ == "__main__":
    main()
