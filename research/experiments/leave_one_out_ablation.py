"""EXP-013: leave-one-channel-out ablation over the TRUE 6 channels, with bootstrap CIs (RQ2).

The manuscript ablation mixes a legacy 5-signal set (audit B10). This is a production-aligned
6-channel ablation: for each channel c, drop c and renormalize the remaining 5 weights to sum 1,
re-score all 30x15 pairs, rank per resume, and measure nDCG@5. The paired drop (full - leave-c),
with a bootstrap CI over the 30 queries, quantifies how load-bearing each channel is. Also reports
single-channel-only nDCG@5. No manuscript edits.

Run: cd backend && PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/leave_one_out_ablation.py
"""
from __future__ import annotations
import json
from pathlib import Path

import numpy as np

from config import Settings
from core.scoring import COMPOSITE_WEIGHTS
from benchmarks.eval_data import load_eval_labels
from benchmarks.extended_evaluation import compute_features, load_settings_data, bootstrap_ci
from benchmarks.metrics import ndcg_at_k

REPO = Path(__file__).resolve().parents[2]
SEED = 42
TOP_K = 5
CHAN = ["semantic", "skills", "title", "experience", "compensation", "remote"]


def score(chan_vals: dict, weights: dict) -> float:
    return sum(weights[c] * chan_vals[c] for c in weights)


def per_query_ndcg(per_cv, weights):
    out = []
    for cv in per_cv:
        relmap = cv["relmap"]
        if not any(r > 0 for r in relmap.values()):
            continue
        scored = [(jid, score(ch, weights)) for jid, ch in cv["rows"]]
        ranking = [jid for jid, _ in sorted(scored, key=lambda t: -t[1])]
        out.append(ndcg_at_k(ranking, relmap, TOP_K))
    return out


def main() -> None:
    np.random.seed(SEED)
    settings = Settings()
    eval_map = load_eval_labels(settings.data_dir / "eval_pairs.json")
    cvs, jobs = load_settings_data(settings)
    model = "all-MiniLM-L6-v2"

    per_cv = []
    for cv in cvs:
        relmap = eval_map.get(cv["id"], {})
        rows = []
        for job in jobs:
            ch = compute_features(cv, job, model, settings)["channels"]
            rows.append((job["id"], {c: ch[c] for c in CHAN}))
        per_cv.append({"qid": cv["id"], "rows": rows, "relmap": relmap})

    full_w = dict(COMPOSITE_WEIGHTS)
    full_q = per_query_ndcg(per_cv, full_w)
    full_mean = float(np.mean(full_q))

    results = {"full_composite_ndcg_at_5": round(full_mean, 6),
               "full_ci": bootstrap_ci(full_q, n_boot=2000),
               "weights": full_w, "leave_one_out": {}, "single_channel": {}}

    for c in CHAN:
        # leave-one-out: drop c, renormalize remaining 5
        rem = {k: v for k, v in full_w.items() if k != c}
        s = sum(rem.values()); rem = {k: v / s for k, v in rem.items()}
        loo_q = per_query_ndcg(per_cv, rem)
        # paired drop full - loo, per query
        drop = [f - l for f, l in zip(full_q, loo_q)]
        results["leave_one_out"][c] = {
            "ndcg_at_5": round(float(np.mean(loo_q)), 6),
            "drop_vs_full_mean": round(float(np.mean(drop)), 6),
            "drop_ci": bootstrap_ci(drop, n_boot=2000),
        }
        # single-channel only
        one_q = per_query_ndcg(per_cv, {c: 1.0})
        results["single_channel"][c] = {"ndcg_at_5": round(float(np.mean(one_q)), 6)}

    # rank channels by how much removing them hurts (positive drop = load-bearing)
    ranked = sorted(CHAN, key=lambda c: -results["leave_one_out"][c]["drop_vs_full_mean"])
    results["channels_by_importance_desc"] = [
        {"channel": c, "drop_vs_full": results["leave_one_out"][c]["drop_vs_full_mean"],
         "drop_ci": results["leave_one_out"][c]["drop_ci"]} for c in ranked
    ]
    results["experiment"] = "EXP-013 leave-one-channel-out ablation (6-channel, RQ2)"
    results["interpretation"] = (
        "drop_vs_full > 0 with a CI excluding 0 => that channel is statistically load-bearing. "
        "Channels whose removal does not significantly change nDCG are not carrying the ranking on "
        "this corpus; report which are load-bearing rather than asserting all six matter."
    )

    outdir = REPO / "research" / "results"; outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "leave_one_out_ablation.json").write_text(json.dumps(results, indent=2))
    print(json.dumps({"full": results["full_composite_ndcg_at_5"],
                      "by_importance": results["channels_by_importance_desc"],
                      "single_channel": {c: results["single_channel"][c]["ndcg_at_5"] for c in CHAN}}, indent=2))


if __name__ == "__main__":
    main()
