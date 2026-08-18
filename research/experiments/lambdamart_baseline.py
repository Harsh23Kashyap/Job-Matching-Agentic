"""EXP-014a: LambdaMART (XGBRanker, listwise rank:ndcg) held-out baseline (RQ1; audit H4/H8).

A GENUINE learning-to-rank baseline (not the pointwise LogReg): XGBRanker with a listwise
rank:ndcg objective on the 6 channel features, 5-fold CV over resumes (held-out). Uses graded
relevance (0/1/2). Reports nDCG@5 with bootstrap CI, compared to the fixed composite (0.949),
the held-out pointwise LR (0.917), and the dense two-tower / semantic bi-encoder (0.878).

Run: cd backend && PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/lambdamart_baseline.py
"""
from __future__ import annotations
import json
from pathlib import Path

import numpy as np
from xgboost import XGBRanker

from config import Settings
from benchmarks.eval_data import load_eval_labels
from benchmarks.extended_evaluation import compute_features, load_settings_data, bootstrap_ci
from benchmarks.metrics import ndcg_at_k

REPO = Path(__file__).resolve().parents[2]
SEED = 42
TOP_K = 5
CHAN = ["semantic", "skills", "title", "experience", "compensation", "remote"]


def main() -> None:
    np.random.seed(SEED)
    settings = Settings()
    eval_map = load_eval_labels(settings.data_dir / "eval_pairs.json")
    cvs, jobs = load_settings_data(settings)
    model_name = "all-MiniLM-L6-v2"

    # rows grouped by resume (contiguous); graded relevance labels
    per_cv = []
    for cv in cvs:
        relmap = eval_map.get(cv["id"], {})
        feats = []
        for job in jobs:
            ch = compute_features(cv, job, model_name, settings)["channels"]
            feats.append(([ch[c] for c in CHAN], int(relmap.get(job["id"], 0)), job["id"]))
        per_cv.append({"qid": cv["id"], "feats": feats, "relmap": relmap})

    idx = np.arange(len(cvs)); np.random.shuffle(idx)
    folds = np.array_split(idx, 5)

    fold_ndcg = []
    for fold in folds:
        val = set(fold.tolist())
        # training rows grouped by resume (contiguous qid), skip empty-label resumes
        X_tr, y_tr, qid_tr = [], [], []
        for ri, cv in enumerate(per_cv):
            if ri in val:
                continue
            if not any(g > 0 for _, g, _ in cv["feats"]):
                continue  # a group with no positive is uninformative for rank:ndcg
            for x, g, _ in cv["feats"]:
                X_tr.append(x); y_tr.append(g); qid_tr.append(ri)
        if len(set(y_tr)) < 2:
            continue
        m = XGBRanker(objective="rank:ndcg", n_estimators=200, max_depth=3,
                      learning_rate=0.1, subsample=0.9, colsample_bytree=0.9,
                      random_state=SEED, tree_method="hist")
        m.fit(np.asarray(X_tr, float), np.asarray(y_tr, int), qid=np.asarray(qid_tr, int))
        for ri in fold:
            cv = per_cv[ri]
            if not any(r > 0 for r in cv["relmap"].values()):
                continue
            Xv = np.asarray([x for x, _, _ in cv["feats"]], float)
            scores = m.predict(Xv)
            ranking = [cv["feats"][j][2] for j in np.argsort(-scores)]
            fold_ndcg.append(ndcg_at_k(ranking, cv["relmap"], TOP_K))

    out = {
        "experiment": "EXP-014a LambdaMART (XGBRanker rank:ndcg) held-out baseline (RQ1)",
        "protocol": "5-fold CV over 30 resumes; listwise rank:ndcg on 6 channel features; graded relevance; seed=42",
        "n_resumes": len(cvs), "n_jobs": len(jobs),
        "lambdamart_ndcg_at_5_mean": round(float(np.mean(fold_ndcg)), 6),
        "lambdamart_ndcg_at_5_ci": bootstrap_ci(fold_ndcg, n_boot=2000),
        "reference": {"fixed_composite": 0.949, "pointwise_LR_heldout": 0.917, "semantic_bi_encoder_two_tower": 0.878},
        "interpretation": (
            "Genuine listwise LTR (LambdaMART) on the same 6 channels, held out over resumes. "
            "Compare honestly to the fixed composite (0.949) and pointwise LR (0.917): report whether "
            "a stronger learned ranker beats the hand-set composite on this small corpus (CIs will be wide)."
        ),
    }
    outdir = REPO / "research" / "results"; outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "lambdamart_baseline.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
