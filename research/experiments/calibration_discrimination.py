"""EXP-020: calibration DISCRIMINATION evidence (audit B8).

A low ECE can hide a near-degenerate confidence that just predicts the base rate.
This adds, on the SAME held-out 5-fold Platt protocol as calibration_binary.json:
  - Brier skill score (BSS) vs the base-rate predictor  -> ~0 means "no better than base rate"
  - ROC-AUC of the calibrated probability                -> does confidence SEPARATE relevant/irrelevant?
  - the distribution of emitted confidences              -> are they near-constant near the base rate?
It does NOT modify calibration_binary.json. Additive, honest RQ3 evidence.

Run: cd backend && PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/calibration_discrimination.py
"""
from __future__ import annotations
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

from config import Settings
from core.calibration import PlattCalibrator
from benchmarks.eval_data import load_eval_labels
from benchmarks.extended_evaluation import compute_features, load_settings_data

REPO = Path(__file__).resolve().parents[2]
SEED = 42


def main() -> None:
    np.random.seed(SEED)
    settings = Settings()
    eval_map = load_eval_labels(settings.data_dir / "eval_pairs.json")
    cvs, jobs = load_settings_data(settings)
    model_name = "all-MiniLM-L6-v2"

    scores, labels, queries = [], [], []
    for cv in cvs:
        rel = eval_map.get(cv["id"], {})
        for job in jobs:
            scores.append(compute_features(cv, job, model_name, settings)["composite"])
            labels.append(1 if rel.get(job["id"], 0) >= 1 else 0)
            queries.append(cv["id"])
    scores = np.asarray(scores, np.float64)
    labels = np.asarray(labels, np.int64)
    base_rate = float(labels.mean())

    uq = sorted(set(queries))
    idx = np.arange(len(uq)); np.random.shuffle(idx)
    folds = np.array_split(idx, 5)

    p_all, y_all = [], []
    for fi in folds:
        val_q = {uq[i] for i in fi}
        tr = np.array([q not in val_q for q in queries]); va = ~tr
        if len(np.unique(labels[tr])) < 2 or len(np.unique(labels[va])) < 2:
            continue
        cal = PlattCalibrator.fit(scores[tr], labels[tr])
        p = np.array([cal.calibrate(float(s)) for s in scores[va]])
        p_all.append(p); y_all.append(labels[va])
    p_all = np.concatenate(p_all); y_all = np.concatenate(y_all)

    brier_model = float(np.mean((p_all - y_all) ** 2))
    brier_base = float(base_rate * (1.0 - base_rate))            # constant base-rate predictor
    bss = 1.0 - brier_model / brier_base if brier_base > 0 else 0.0
    try:
        auc = float(roc_auc_score(y_all, p_all))
    except ValueError:
        auc = None
    # confidence distribution
    pct = {f"p{q}": float(np.percentile(p_all, q)) for q in (10, 25, 50, 75, 90)}
    hist_edges = np.linspace(0, 1, 11)
    hist = np.histogram(p_all, bins=hist_edges)[0].tolist()

    out = {
        "experiment": "EXP-020 calibration discrimination (B8)",
        "protocol": "held-out 5-fold Platt over resumes; pooled val predictions; seed=42",
        "n_pairs": int(len(y_all)), "base_rate_positive": round(base_rate, 6),
        "brier_model": round(brier_model, 6), "brier_baserate_predictor": round(brier_base, 6),
        "brier_skill_score": round(bss, 6),
        "roc_auc": round(auc, 6) if auc is not None else None,
        "confidence_mean": round(float(p_all.mean()), 6),
        "confidence_std": round(float(p_all.std()), 6),
        "confidence_min": round(float(p_all.min()), 6),
        "confidence_max": round(float(p_all.max()), 6),
        "confidence_percentiles": {k: round(v, 6) for k, v in pct.items()},
        "confidence_histogram_0to1_10bins": hist,
        "interpretation": (
            "BSS ~ 0 => calibrated confidence is barely better than predicting the base rate; "
            "AUC quantifies whether confidence separates relevant from irrelevant; a narrow "
            "confidence range near the base rate indicates near-degenerate (low-discrimination) confidence."
        ),
    }
    outdir = REPO / "research" / "results"; outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "calibration_discrimination.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
