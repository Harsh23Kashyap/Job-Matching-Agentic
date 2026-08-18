"""EXP-012: JOB-held-out generalization (Phase 4 / RQ7; audit H3).

The manuscript's k-fold holds out RESUMES only (all 15 jobs in every fold) and is
vacuous for the FIXED-weight composite (nothing is learned). This tests generalization
to UNSEEN JOBS for the LEARNED pointwise LTR: partition the 15 jobs into folds, train
the LTR only on (resume, job) pairs whose job is NOT held out, then rank ALL 15 jobs
per resume and score nDCG@5. Reports:
  - overall (all resumes, all folds)
  - STRICT subset (resume-folds where >=1 of the resume's relevant jobs is held out) <- the honest generalization number
  - fixed composite reference (constant; not trained -> job-held-out is descriptive only)

Run: cd backend && PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/job_heldout.py
"""
from __future__ import annotations
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression

from config import Settings
from benchmarks.eval_data import load_eval_labels
from benchmarks.extended_evaluation import compute_features, load_settings_data, bootstrap_ci
from benchmarks.metrics import ndcg_at_k, precision_at_k, recall_at_k

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
    job_ids = [j["id"] for j in jobs]

    # per-resume rows: (job_id, feature_vector[6], binary_label, composite_score)
    per_cv = []
    for cv in cvs:
        relmap = eval_map.get(cv["id"], {})
        rows = []
        for job in jobs:
            f = compute_features(cv, job, model_name, settings)
            x = [f["channels"][c] for c in CHAN]
            rows.append((job["id"], x, 1 if relmap.get(job["id"], 0) >= 1 else 0, f["composite"]))
        per_cv.append({"qid": cv["id"], "rows": rows, "relmap": relmap})

    # 5 job-folds over the 15 jobs
    jidx = np.arange(len(jobs)); np.random.shuffle(jidx)
    folds = np.array_split(jidx, 5)

    overall_ndcg, overall_p, overall_r = [], [], []
    strict_ndcg = []          # resume-folds where >=1 relevant job is held out
    n_strict_pairs = 0
    for fold in folds:
        heldout = {job_ids[i] for i in fold}
        # train on non-held-out jobs
        Xtr, ytr = [], []
        for cv in per_cv:
            for jid, x, yb, _ in cv["rows"]:
                if jid not in heldout:
                    Xtr.append(x); ytr.append(yb)
        if len(set(ytr)) < 2:
            continue
        clf = LogisticRegression(max_iter=1000, C=1.0, random_state=SEED)
        clf.fit(np.asarray(Xtr, float), np.asarray(ytr, int))
        for cv in per_cv:
            relmap = cv["relmap"]
            if not any(r > 0 for r in relmap.values()):
                continue
            Xall = np.asarray([x for _, x, _, _ in cv["rows"]], float)
            scores = clf.predict_proba(Xall)[:, 1]
            ranking = [cv["rows"][j][0] for j in np.argsort(-scores)]
            n = ndcg_at_k(ranking, relmap, TOP_K)
            pos = {d: r for d, r in relmap.items() if r > 0}
            overall_ndcg.append(n)
            overall_p.append(precision_at_k(ranking, pos, TOP_K))
            overall_r.append(recall_at_k(ranking, pos, TOP_K))
            # strict: does this resume have a relevant job among the held-out jobs?
            if any((d in heldout) for d in pos):
                strict_ndcg.append(n); n_strict_pairs += 1

    # fixed composite reference (constant; ranks all 15 by composite)
    comp_ndcg = []
    for cv in per_cv:
        relmap = cv["relmap"]
        if not any(r > 0 for r in relmap.values()):
            continue
        ranking = [cv["rows"][j][0] for j in np.argsort(-np.asarray([c for _, _, _, c in cv["rows"]]))]
        comp_ndcg.append(ndcg_at_k(ranking, relmap, TOP_K))

    out = {
        "experiment": "EXP-012 job-held-out generalization (RQ7)",
        "protocol": "5 folds over 15 jobs; LTR trained on non-held-out jobs; rank all 15 per resume; seed=42",
        "n_jobs": len(jobs), "n_resumes": len(cvs),
        "ltr_jobheldout_ndcg_at_5_mean": round(float(np.mean(overall_ndcg)), 6),
        "ltr_jobheldout_ndcg_at_5_ci": bootstrap_ci(overall_ndcg, n_boot=2000),
        "ltr_jobheldout_p_at_5_mean": round(float(np.mean(overall_p)), 6),
        "ltr_jobheldout_r_at_5_mean": round(float(np.mean(overall_r)), 6),
        "ltr_STRICT_heldout_relevant_ndcg_at_5_mean": round(float(np.mean(strict_ndcg)), 6) if strict_ndcg else None,
        "ltr_STRICT_heldout_relevant_ndcg_at_5_ci": bootstrap_ci(strict_ndcg, n_boot=2000) if strict_ndcg else None,
        "n_strict_resume_fold_pairs": n_strict_pairs,
        "fixed_composite_reference_ndcg_at_5_mean": round(float(np.mean(comp_ndcg)), 6),
        "compare_resume_heldout_ltr": "pointwise_ltr.json ndcg@5=0.917 (resume folds); composite kfold=0.949",
        "interpretation": (
            "The STRICT number (resumes whose relevant job was held out of LTR training) is the honest "
            "unseen-job generalization measure. The fixed composite is not trained, so its 'job-held-out' "
            "value is descriptive, not generalization. If STRICT << overall, the learned model does not "
            "generalize to unseen jobs and the composite/held-out numbers should be reported with that caveat."
        ),
    }
    outdir = REPO / "research" / "results"; outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "job_heldout.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
