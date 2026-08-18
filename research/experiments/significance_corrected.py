"""EXP-022 / Phase 27: reproducible significance + multiple-comparison correction.

Re-runs the paired bootstrap on the COMMITTED per-query nDCG (ablation_per_query.csv) using the
FIXED deterministic seed (B3), then applies Holm-Bonferroni across the family of comparisons vs the
semantic baseline and reports TWO-SIDED p. Addresses the audit: borderline p=0.048, one-sided,
uncorrected, non-reproducible seed. No re-scoring (uses committed per-query data).

Run: cd backend && PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/significance_corrected.py
"""
from __future__ import annotations
import csv
import json
from pathlib import Path

from benchmarks.significance import run_significance_analysis

REPO = Path(__file__).resolve().parents[2]
PQ = REPO / "backend" / "reports" / "research_run_20260606T150509Z" / "ablation_per_query.csv"
BASELINE = "semantic_only"


def holm(pvals):
    # returns dict idx->(adjusted_alpha_rank, reject@0.05) via Holm-Bonferroni
    idx = sorted(range(len(pvals)), key=lambda i: pvals[i])
    m = len(pvals)
    out = {}
    still = True
    for rank, i in enumerate(idx):
        thresh = 0.05 / (m - rank)
        rej = still and (pvals[i] <= thresh)
        if not rej:
            still = False
        out[i] = {"holm_threshold": round(thresh, 5), "reject_holm_0.05": bool(rej)}
    return out


def main() -> None:
    rows = []
    with open(PQ) as f:
        for r in csv.DictReader(f):
            rows.append({
                "method_key": r["variant_key"], "method": r["variant"], "query_id": r["query_id"],
                "ndcg_at_k": float(r["ndcg_at_k"]), "mrr": float(r["mrr"]),
            })
    report = run_significance_analysis(rows, baseline_key=BASELINE, top_k=5)

    ndcg_cmps = [c for c in report.comparisons if c["metric"] == "ndcg_at_k"]
    pv = [c["p_value"] for c in ndcg_cmps]           # one-sided
    hol = holm(pv)
    out_cmps = []
    for i, c in enumerate(ndcg_cmps):
        two_sided = min(1.0, 2.0 * c["p_value"]) if c["mean_diff"] >= 0 else min(1.0, 2.0 * (1 - c["p_value"]))
        out_cmps.append({
            "compare": c["compare"], "mean_diff": c["mean_diff"],
            "ci95": [c["ci95_lo"], c["ci95_hi"]],
            "p_one_sided": c["p_value"], "p_two_sided": round(two_sided, 4),
            "wins_losses_ties": f"{c['wins']}/{c['losses']}/{c['ties']}",
            **hol[i],
        })
    out_cmps.sort(key=lambda x: x["p_one_sided"])

    composite = next((c for c in out_cmps if "composite" in c["compare"].lower()), None)
    out = {
        "experiment": "EXP-022 / Phase 27 significance + Holm correction (baseline: semantic)",
        "source": "committed ablation_per_query.csv; deterministic seed (B3 fix); paired bootstrap N=5000",
        "family_size": len(ndcg_cmps),
        "comparisons_ndcg": out_cmps,
        "headline_full_composite_vs_semantic": composite,
        "interpretation": (
            "p is now reproducible (fixed seed). Report TWO-SIDED p and Holm-corrected significance. "
            "Comparisons whose CI includes 0 or that fail Holm are NOT robust; the composite-vs-semantic "
            "headline should be described accordingly rather than as a bare 'p<0.05'."
        ),
    }
    outdir = REPO / "research" / "results"; outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "significance_corrected.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({"headline": composite, "n_comparisons": len(ndcg_cmps),
                      "survive_holm": [c["compare"] for c in out_cmps if c["reject_holm_0.05"]]}, indent=2))


if __name__ == "__main__":
    main()
