"""EXP-026 / Stage-2 §N: calibration-method comparison with a DEFINED probability target.

Probability target (stated explicitly, removing the "confidence" ambiguity in the audit):
    p_ij = P(y_ij = 1 | s_ij),  y_ij = 1  iff  graded relevance >= 1 (relevant or strong),
    s_ij = the fixed 6-channel composite score.

Compares four calibration maps on a HELD-OUT 5-fold protocol over resumes (fit on train folds,
evaluate on pooled held-out predictions — never fit on test):
    raw          : use the composite score directly as a probability (uncalibrated baseline)
    platt        : sigmoid(a*s + b), 2 params, fit by gradient descent (core.PlattCalibrator)
    isotonic     : non-parametric monotone map (sklearn IsotonicRegression)
    temperature  : sigmoid(s / T), 1 param, T fit by NLL minimization
Reports per method: ECE (10-bin), MCE, Brier, Brier-skill-score vs the base-rate constant,
ROC-AUC (discrimination), reliability curve, and a bootstrap CI on ECE. Also reports the trivial
CONSTANT base-rate predictor as the floor (Stage-2 §N: "test vs a trivial constant predictor").

Run: cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false \
  PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/calibration_methods.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from config import Settings
from core.calibration import PlattCalibrator
from benchmarks.eval_data import load_eval_labels
from benchmarks.extended_evaluation import compute_features, load_settings_data

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "research" / "results" / "calibration_methods.json"
SEED = 42


def ece_mce(p, y, n_bins=10):
    edges = np.linspace(0, 1, n_bins + 1)
    ece = mce = 0.0
    curve = []
    for i in range(n_bins):
        lo, hi = edges[i], edges[i + 1]
        m = (p >= lo) & (p < hi) if i < n_bins - 1 else (p >= lo) & (p <= hi)
        if not m.any():
            curve.append({"bin": [round(lo, 2), round(hi, 2)], "n": 0, "mean_pred": None, "frac_pos": None})
            continue
        conf = float(p[m].mean()); acc = float(y[m].mean()); w = m.mean()
        gap = abs(conf - acc)
        ece += w * gap
        mce = max(mce, gap)
        curve.append({"bin": [round(lo, 2), round(hi, 2)], "n": int(m.sum()),
                      "mean_pred": round(conf, 4), "frac_pos": round(acc, 4)})
    return float(ece), float(mce), curve


def ece_adaptive(p, y, n_bins=10):
    """Adaptive (equal-mass) ECE: bins hold ~equal counts (quantile edges). More robust than
    equal-width bins when predictions cluster in a narrow range (Nixon et al. 2019)."""
    n = len(p)
    if n == 0:
        return 0.0
    order = np.argsort(p)
    ece = 0.0
    for chunk in np.array_split(order, min(n_bins, n)):
        if len(chunk) == 0:
            continue
        conf = float(p[chunk].mean()); acc = float(y[chunk].mean())
        ece += (len(chunk) / n) * abs(conf - acc)
    return float(ece)


def fit_beta(scores, labels):
    """Beta calibration (Kull et al. 2017): logistic regression on features [ln s, -ln(1-s)],
    a principled 3-parameter map for scores already in (0,1). Generalizes Platt/logistic."""
    s = np.clip(scores, 1e-6, 1 - 1e-6)
    X = np.column_stack([np.log(s), -np.log(1 - s)])
    lr = LogisticRegression(max_iter=1000, C=1e6)  # near-unregularized: it is a 2-feature fit
    lr.fit(X, labels)
    return lr


def apply_beta(lr, scores):
    s = np.clip(scores, 1e-6, 1 - 1e-6)
    X = np.column_stack([np.log(s), -np.log(1 - s)])
    return np.clip(lr.predict_proba(X)[:, 1], 0, 1)


def fit_temperature(scores, labels, grid=None):
    """1-param temperature: p = sigmoid(s / T); pick T minimizing NLL on train."""
    grid = grid if grid is not None else np.linspace(0.02, 2.0, 100)
    y = labels.astype(float)
    best_T, best_nll = 1.0, np.inf
    for T in grid:
        z = np.clip(scores / T, -500, 500)
        p = 1.0 / (1.0 + np.exp(-z))
        p = np.clip(p, 1e-7, 1 - 1e-7)
        nll = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
        if nll < best_nll:
            best_nll, best_T = nll, T
    return best_T


def bootstrap_ece_ci(p, y, n_boot=2000, seed=SEED):
    rng = np.random.default_rng(seed)
    n = len(p)
    vals = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        e, _, _ = ece_mce(p[idx], y[idx])
        vals.append(e)
    return {"ci_low": round(float(np.quantile(vals, 0.025)), 4), "ci_high": round(float(np.quantile(vals, 0.975)), 4)}


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

    preds = {"raw": [], "platt": [], "isotonic": [], "temperature": [], "beta": []}
    ys = []
    for fi in folds:
        val_q = {uq[i] for i in fi}
        tr = np.array([q not in val_q for q in queries]); va = ~tr
        if len(np.unique(labels[tr])) < 2 or len(np.unique(labels[va])) < 2:
            continue
        s_tr, y_tr, s_va = scores[tr], labels[tr], scores[va]
        # raw
        preds["raw"].append(np.clip(s_va, 0, 1))
        # platt
        cal = PlattCalibrator.fit(s_tr, y_tr)
        preds["platt"].append(np.array([cal.calibrate(float(s)) for s in s_va]))
        # isotonic
        iso = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
        iso.fit(s_tr, y_tr)
        preds["isotonic"].append(np.clip(iso.predict(s_va), 0, 1))
        # temperature
        T = fit_temperature(s_tr, y_tr)
        preds["temperature"].append(1.0 / (1.0 + np.exp(-np.clip(s_va / T, -500, 500))))
        # beta calibration (Kull et al. 2017)
        preds["beta"].append(apply_beta(fit_beta(s_tr, y_tr), s_va))
        ys.append(labels[va])

    y_all = np.concatenate(ys)
    results = {}
    for method, chunks in preds.items():
        p = np.concatenate(chunks)
        ece, mce, curve = ece_mce(p, y_all)
        a_ece = ece_adaptive(p, y_all)
        brier = float(np.mean((p - y_all) ** 2))
        brier_base = base_rate * (1 - base_rate)
        bss = 1 - brier / brier_base if brier_base > 0 else 0.0
        try:
            auc = float(roc_auc_score(y_all, p))
        except ValueError:
            auc = None
        results[method] = {
            "ece": round(ece, 4), "ece_ci": bootstrap_ece_ci(p, y_all),
            "adaptive_ece": round(a_ece, 4),
            "mce": round(mce, 4), "brier": round(brier, 4), "brier_skill_score": round(bss, 4),
            "roc_auc": round(auc, 4) if auc is not None else None,
            "confidence_range": [round(float(p.min()), 4), round(float(p.max()), 4)],
            "reliability_curve": curve,
        }

    # trivial constant base-rate predictor (floor)
    p_const = np.full_like(y_all, base_rate, dtype=float)
    ece_c, mce_c, _ = ece_mce(p_const, y_all)
    results["constant_base_rate"] = {
        "ece": round(ece_c, 4), "mce": round(mce_c, 4),
        "brier": round(float(np.mean((p_const - y_all) ** 2)), 4), "brier_skill_score": 0.0,
        "roc_auc": 0.5, "note": "trivial floor: always predicts the base rate",
    }

    best = min([m for m in ("raw", "platt", "isotonic", "temperature", "beta")], key=lambda m: results[m]["ece"])
    best_adaptive = min([m for m in ("raw", "platt", "isotonic", "temperature", "beta")], key=lambda m: results[m]["adaptive_ece"])
    out = {
        "experiment": "EXP-026 calibration methods with defined target (Stage-2 §N)",
        "probability_target": "p_ij = P(y=1 | s_ij); y=1 iff graded relevance >= 1; s = fixed 6-channel composite",
        "protocol": "held-out 5-fold over resumes (fit on train, pooled held-out eval); seed 42; never fit on test",
        "n_pairs": int(len(y_all)), "base_rate_positive": round(base_rate, 4),
        "methods": results,
        "lowest_ece_method": best,
        "lowest_adaptive_ece_method": best_adaptive,
        "interpretation": (
            "Report ECE alongside Brier-skill-score and AUC: a low ECE is only meaningful if the model also "
            "DISCRIMINATES (BSS>0, AUC>0.5) — otherwise it is near the trivial constant base-rate predictor. "
            "We add ADAPTIVE (equal-mass) ECE because the composite scores cluster in a narrow band, so "
            "equal-width bins are mostly empty and can understate miscalibration; adaptive ECE is the more "
            "honest aggregate here. We also add BETA calibration (Kull et al. 2017), the principled [0,1]-score "
            "generalization of Platt. Prefer the simplest map unless a richer one materially and reproducibly "
            "improves BOTH calibration and discrimination without overfitting the tiny calibration set."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps({k: {kk: results[k].get(kk) for kk in ("ece", "brier", "brier_skill_score", "roc_auc", "confidence_range")}
                      for k in results}, indent=2))
    print("lowest ECE:", best, "| base rate:", round(base_rate, 4))


if __name__ == "__main__":
    main()
