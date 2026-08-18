"""EXP-027 / Stage-2 §J: generalization suite — unseen-candidate, unseen-job, BOTH-unseen.

Measures generalization of the LEARNED pointwise fusion (LogReg on the 6 channels) under three
held-out regimes with ZERO leakage. In EVERY regime the model ranks the SAME full 15-job pool per
resume (so nDCG@5 / recall@5 are commensurable with the fixed-composite reference, 0.949); the
"unseen" property comes only from the TRAINING exclusion, not from shrinking the ranking pool
(code-review fix: previously job/both-unseen ranked only the ~3 held-out jobs, which made nDCG@5 a
3-item score and recall@5 trivially 1.0 — not comparable to the 15-job composite).

  candidate_heldout : train LTR on TRAIN resumes; each held-out resume evaluated ONCE (ranks 15 jobs).
  job_heldout       : train LTR on non-held-out job columns; STRICT = resumes whose relevant job is in
                      the held-out fold (the honest unseen-job measure), ranking all 15 jobs.
  both_heldout      : train on (seen resume x seen job); evaluate held-out resumes whose relevant job is
                      also held out (STRICT), ranking all 15 jobs.

Bootstrap CIs are over ONE value PER RESUME (per-resume aggregation before resampling), so n reflects
the true number of independent query units, not pseudo-replicated fold repeats.

Run: cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false \
  PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/generalization.py
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression

from config import Settings
from benchmarks.eval_data import load_eval_labels
from benchmarks.extended_evaluation import compute_features, load_settings_data
from core.scoring import COMPOSITE_WEIGHTS
from benchmarks.metrics import ndcg_at_k, recall_at_k

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "research" / "results" / "generalization.json"
SEED = 42
CHAN = ["semantic", "skills", "title", "experience", "compensation", "remote"]
TOP_K = 5


def bootstrap_ci(vals, n_boot=2000, seed=SEED):
    rng = np.random.default_rng(seed)
    arr = np.asarray(vals, float)
    if len(arr) == 0:
        return {"mean": None, "ci_low": None, "ci_high": None, "n_queries": 0}
    boots = np.array([arr[rng.integers(0, len(arr), len(arr))].mean() for _ in range(n_boot)])
    return {"mean": round(float(arr.mean()), 6), "ci_low": round(float(np.quantile(boots, 0.025)), 6),
            "ci_high": round(float(np.quantile(boots, 0.975)), 6), "n_queries": len(arr)}


def main() -> None:
    np.random.seed(SEED)
    settings = Settings()
    eval_map = load_eval_labels(settings.data_dir / "eval_pairs.json")
    cvs, jobs = load_settings_data(settings)
    model_name = "all-MiniLM-L6-v2"
    job_ids = [j["id"] for j in jobs]
    n_j = len(jobs)
    all_ji = list(range(n_j))

    feat = {}
    for ci, cv in enumerate(cvs):
        rel = eval_map.get(cv["id"], {})
        for ji, job in enumerate(jobs):
            ch = compute_features(cv, job, model_name, settings)["channels"]
            g = int(rel.get(job["id"], 0))
            feat[(ci, ji)] = ([ch[c] for c in CHAN], g, 1 if g >= 1 else 0)

    def fit_ltr(train_pairs):
        X = [feat[p][0] for p in train_pairs]
        y = [feat[p][2] for p in train_pairs]
        if len(set(y)) < 2:
            return None
        clf = LogisticRegression(max_iter=1000, C=1.0, random_state=SEED)
        clf.fit(np.asarray(X, float), np.asarray(y, int))
        return clf

    def score_query(clf, ci):
        """Rank ALL 15 jobs for resume ci; return (ndcg@5, recall@5) or None if no positives."""
        relmap = {job_ids[ji]: feat[(ci, ji)][1] for ji in all_ji}
        pos = {d: r for d, r in relmap.items() if r > 0}
        if not pos:
            return None
        X = np.asarray([feat[(ci, ji)][0] for ji in all_ji], float)
        scores = clf.predict_proba(X)[:, 1]
        ranking = [job_ids[ji] for ji in np.argsort(-scores)]
        return ndcg_at_k(ranking, relmap, TOP_K), recall_at_k(ranking, pos, TOP_K)

    ridx = np.arange(len(cvs)); np.random.shuffle(ridx)
    r_folds = np.array_split(ridx, 5)
    jidx = np.arange(n_j); np.random.shuffle(jidx)
    j_folds = np.array_split(jidx, 5)

    regimes = {}

    # 1) candidate held-out: each resume scored once, all 15 jobs
    nd, rc, leak_ok = [], [], True
    for fold in r_folds:
        val = set(int(i) for i in fold)
        train_pairs = [(ci, ji) for ci in range(len(cvs)) if ci not in val for ji in all_ji]
        clf = fit_ltr(train_pairs)
        if clf is None:
            continue
        if any(p[0] in val for p in train_pairs):
            leak_ok = False
        for ci in val:
            r = score_query(clf, ci)
            if r:
                nd.append(r[0]); rc.append(r[1])
    regimes["candidate_heldout"] = {"ltr_ndcg@5": bootstrap_ci(nd),
                                    "ltr_recall@5_mean": round(float(np.mean(rc)), 6) if rc else None,
                                    "pool_size": n_j, "leakage_check_disjoint": leak_ok,
                                    "desc": "LTR trained on train resumes; each UNSEEN resume ranks all 15 jobs, scored once"}

    # 2) job held-out (STRICT): rank all 15; count resumes whose relevant job is in the held-out fold
    per_resume = defaultdict(list)
    leak_ok = True
    for fold in j_folds:
        valj = set(int(i) for i in fold)
        train_pairs = [(ci, ji) for ci in range(len(cvs)) for ji in all_ji if ji not in valj]
        clf = fit_ltr(train_pairs)
        if clf is None:
            continue
        if any(p[1] in valj for p in train_pairs):
            leak_ok = False
        for ci in range(len(cvs)):
            # STRICT: this resume must have a relevant job among the held-out (unseen) jobs
            if not any((feat[(ci, ji)][1] > 0) for ji in valj):
                continue
            r = score_query(clf, ci)
            if r:
                per_resume[ci].append(r[0])
    nd_job = [float(np.mean(v)) for v in per_resume.values()]
    regimes["job_heldout"] = {"ltr_ndcg@5": bootstrap_ci(nd_job), "pool_size": n_j,
                              "leakage_check_disjoint": leak_ok,
                              "desc": "STRICT unseen-job: LTR trained on seen job columns; resumes with a relevant HELD-OUT job rank all 15; per-resume aggregated"}

    # 3) both held-out (STRICT): unseen resume AND relevant job unseen; rank all 15
    per_resume = defaultdict(list)
    leak_ok = True
    for rf in r_folds:
        valr = set(int(i) for i in rf)
        for jf in j_folds:
            valj = set(int(i) for i in jf)
            train_pairs = [(ci, ji) for ci in range(len(cvs)) if ci not in valr
                           for ji in all_ji if ji not in valj]
            clf = fit_ltr(train_pairs)
            if clf is None:
                continue
            if any((p[0] in valr) or (p[1] in valj) for p in train_pairs):
                leak_ok = False
            for ci in valr:
                if not any((feat[(ci, ji)][1] > 0) for ji in valj):
                    continue
                r = score_query(clf, ci)
                if r:
                    per_resume[ci].append(r[0])
    nd_both = [float(np.mean(v)) for v in per_resume.values()]
    regimes["both_heldout"] = {"ltr_ndcg@5": bootstrap_ci(nd_both), "pool_size": n_j,
                               "leakage_check_disjoint": leak_ok,
                               "desc": "STRICT both-unseen: train on (seen resume x seen job); UNSEEN resumes with a relevant UNSEEN job rank all 15; per-resume aggregated"}

    # fixed composite reference (not trained; ranks all 15)
    comp_nd = []
    for ci, cv in enumerate(cvs):
        relmap = {job_ids[ji]: feat[(ci, ji)][1] for ji in all_ji}
        pos = {d: r for d, r in relmap.items() if r > 0}
        if not pos:
            continue
        scored = [(job_ids[ji], sum(COMPOSITE_WEIGHTS[c] * v for c, v in zip(CHAN, feat[(ci, ji)][0]))) for ji in all_ji]
        ranking = [d for d, _ in sorted(scored, key=lambda x: -x[1])]
        comp_nd.append(ndcg_at_k(ranking, relmap, TOP_K))
    regimes["fixed_composite_reference"] = {"ndcg@5": bootstrap_ci(comp_nd), "pool_size": n_j,
                                            "desc": "fixed composite ranking all 15 jobs (not trained -> descriptive)"}

    out = {
        "experiment": "EXP-027 generalization: unseen-candidate / unseen-job / both-unseen (Stage-2 §J)",
        "seed": SEED, "n_resumes": len(cvs), "n_jobs": n_j,
        "note": "ALL regimes rank the full 15-job pool (commensurable with the composite reference); "
                "unseen-job/both regimes use the STRICT subset (resume has a relevant HELD-OUT job) and "
                "aggregate to one value per resume before bootstrapping (no pseudo-replication).",
        "regimes": regimes,
        "interpretation": (
            "The learned fusion generalizes if the unseen-candidate / unseen-job / both-unseen nDCG@5 stay "
            "close to the fixed composite reference (0.949), all over the same 15-job pool. Zero leakage is "
            "verified programmatically. CIs are wide at n=30 resumes / 15 jobs — report with that caveat."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
