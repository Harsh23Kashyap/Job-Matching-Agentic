"""EXP-015: weight-stability via cluster bootstrap (Phase 7, RQ2).

Are the channel weights stable, or artifacts of 47 labels? Cluster-bootstrap over the 30 resumes
(resample queries with replacement, refit a logistic-regression linear fusion on their pairs),
1000 iters. Report each channel's raw-coefficient mean +/- 95% CI and sign-stability (% of bootstraps
with positive coefficient). Wide CIs or sign flips => the weighting is not stable at this corpus size.
Complements the fixed hand-set weights (0.28/0.27/0.10/0.15/0.10/0.10) and EXP-013 leave-one-out.

Run: cd backend && PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/weight_stability.py
"""
from __future__ import annotations
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression

from config import Settings
from core.scoring import COMPOSITE_WEIGHTS
from benchmarks.eval_data import load_eval_labels
from benchmarks.extended_evaluation import compute_features, load_settings_data

REPO = Path(__file__).resolve().parents[2]
SEED = 42
N_BOOT = 1000
CHAN = ["semantic", "skills", "title", "experience", "compensation", "remote"]


def main() -> None:
    rng = np.random.default_rng(SEED)
    settings = Settings()
    eval_map = load_eval_labels(settings.data_dir / "eval_pairs.json")
    cvs, jobs = load_settings_data(settings)
    model = "all-MiniLM-L6-v2"

    # per-resume feature block + binary labels
    blocks = []
    for cv in cvs:
        relmap = eval_map.get(cv["id"], {})
        X = np.array([[compute_features(cv, j, model, settings)["channels"][c] for c in CHAN] for j in jobs], float)
        y = np.array([1 if relmap.get(j["id"], 0) >= 1 else 0 for j in jobs], int)
        blocks.append((X, y))
    n = len(blocks)

    coefs = []
    for _ in range(N_BOOT):
        pick = rng.integers(0, n, size=n)  # cluster bootstrap over resumes
        Xb = np.vstack([blocks[i][0] for i in pick])
        yb = np.concatenate([blocks[i][1] for i in pick])
        if len(np.unique(yb)) < 2:
            continue
        clf = LogisticRegression(max_iter=1000, C=1.0, random_state=SEED).fit(Xb, yb)
        coefs.append(clf.coef_[0])
    coefs = np.asarray(coefs)  # (B,6)

    per_channel = {}
    for k, c in enumerate(CHAN):
        col = coefs[:, k]
        per_channel[c] = {
            "hand_set_weight": COMPOSITE_WEIGHTS[c],
            "boot_coef_mean": round(float(col.mean()), 4),
            "boot_coef_ci95": [round(float(np.percentile(col, 2.5)), 4), round(float(np.percentile(col, 97.5)), 4)],
            "pct_positive": round(float((col > 0).mean()), 3),
            "sign_stable": bool((col > 0).mean() >= 0.95 or (col < 0).mean() >= 0.95),
        }
    # normalized |coef| as pseudo-weights (mean across bootstraps)
    absmean = np.abs(coefs).mean(0)
    norm_w = (absmean / absmean.sum()).round(3)
    out = {
        "experiment": "EXP-015 weight-stability cluster bootstrap (RQ2)",
        "n_bootstraps": int(len(coefs)), "resamples": "cluster over 30 resumes",
        "per_channel": per_channel,
        "normalized_abs_coef_pseudo_weights": {c: float(norm_w[k]) for k, c in enumerate(CHAN)},
        "hand_set_weights": dict(COMPOSITE_WEIGHTS),
        "interpretation": (
            "sign_stable=false or a wide CI spanning 0 => that channel's contribution is not stable at "
            "n=30 and the hand-set weight is not empirically pinned. Compare the normalized pseudo-weights "
            "to the hand-set weights: large divergence means the 0.28/0.27... vector is a prior, not a fitted optimum."
        ),
    }
    outdir = REPO / "research" / "results"; outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "weight_stability.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
