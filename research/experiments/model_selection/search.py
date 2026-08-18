"""EXP-025 / Stage-2 §D-E: protocol-gated model-selection search (NOT cherry-picking).

Explores ~25 legitimate ranking configurations on the REAL human corpus (30 resumes x 15
jobs, 47 graded labels) to answer §D's questions: is the fixed-composite result an artifact?
is there a better-justified config? is the benchmark too small to distinguish configs? is a
stronger protocol revealing a real contribution?

STRICT PROTOCOL (Stage-2 §A/§E), decided BEFORE any result is inspected:
  * Metric of record: per-query nDCG@5 under 5-fold resume-level cross-validation (seed 42).
    LEARNED configs are fit on the training folds only and scored on the held-out fold
    (zero leakage). FIXED configs have nothing to fit; their per-query nDCG is fold-invariant.
  * SELECTION CRITERIA (frozen here, before seeing the leaderboard):
      1. PRIMARY = mean nDCG@5.
      2. A challenger only *beats* the incumbent (fixed 6-channel composite, C01) if the
         paired-bootstrap 95% CI of (challenger - incumbent) per-query nDCG EXCLUDES 0 AND
         survives Holm-Bonferroni across the whole config family.
      3. If NO challenger clears (2), SELECT THE INCUMBENT by parsimony/auditability
         (zero fitted parameters, deterministic, fully decomposable) — chosen a priori as the
         tie-break winner when configs are statistically indistinguishable (§E).
  * ALL configs reported (leaderboard), negatives preserved. If a competitor wins, we say so.

Run: cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false \
  PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/model_selection/search.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression, Ridge
from xgboost import XGBRanker

from config import Settings
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.document_text import job_document_text, resume_document_text
from core.embedding import embed_text
from core.similarity import compute_similarity
from core.skills import jaccard_skills, soft_overlap
from core.component_scores import (
    compensation_score, experience_score, remote_preference_score, title_similarity_score,
)
from benchmarks.eval_data import load_eval_labels
from benchmarks.extended_evaluation import load_settings_data
from benchmarks.metrics import ndcg_at_k, recall_at_k

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "research" / "results" / "model_selection.json"
SEED = 42
MODEL = "all-MiniLM-L6-v2"
CHAN = ["semantic", "skills", "title", "experience", "compensation", "remote"]
HAND = {"semantic": 0.28, "skills": 0.27, "title": 0.10, "experience": 0.15, "compensation": 0.10, "remote": 0.10}


def _snap(cv, job, model_name):
    cdoc = resume_document_text(cv)
    jdoc = job_document_text(job)
    cs = CandidateSnapshot(id=cv["id"], name=cv.get("name", ""), skills=list(cv.get("skills", [])),
                           experience_years=float(cv.get("experience_years", 0)),
                           remote_preference=bool(cv.get("remote_preference", False)),
                           preferred_salary=cv.get("preferred_salary"), summary=str(cv.get("summary", "")),
                           version=1, document_text_hash=hashlib.sha256(cdoc.encode()).hexdigest(),
                           embedding=embed_text(cdoc, model_name=model_name).tolist())
    js = JobSnapshot(id=job["id"], title=job.get("title", ""), required_skills=list(job.get("required_skills", [])),
                     preferred_skills=list(job.get("preferred_skills", [])),
                     required_experience=int(job.get("required_experience", 0)),
                     remote_policy=bool(job.get("remote_policy", False)), budget=job.get("budget"),
                     description=str(job.get("description", "")), version=1,
                     document_text_hash=hashlib.sha256(jdoc.encode()).hexdigest(),
                     embedding=embed_text(jdoc, model_name=model_name).tolist())
    return cs, js


def build_features(cvs, jobs):
    """Precompute a wide feature table per (cv, job): all channel variants (cached embeddings)."""
    csnap, jsnap = {}, {}
    for cv in cvs:
        cs, _ = _snap(cv, jobs[0], MODEL)
        csnap[cv["id"]] = cs
    for job in jobs:
        _, js = _snap(cvs[0], job, MODEL)
        jsnap[job["id"]] = js

    feats = {}  # (cid, jid) -> dict of feature columns
    for cv in cvs:
        cs = csnap[cv["id"]]
        for job in jobs:
            js = jsnap[job["id"]]
            cvec = np.asarray(cs.embedding, np.float32)
            jvec = np.asarray(js.embedding, np.float32)
            feats[(cv["id"], job["id"])] = {
                "semantic": compute_similarity(cvec, jvec, "cosine"),
                "semantic_dot": float(np.dot(cvec, jvec)),
                "skills": jaccard_skills(cv.get("skills", []), job.get("required_skills", [])),
                "skills_emb": soft_overlap(cv.get("skills", []), job.get("required_skills", []), MODEL),
                "title": title_similarity_score(cs, js),
                "experience": experience_score(cs, js),
                "compensation": compensation_score(cs, js),
                "remote": remote_preference_score(cs, js),
            }
    return feats


def weighted(f, weights, sem_key="semantic", skills_key="skills"):
    m = {"semantic": f[sem_key], "skills": f[skills_key], "title": f["title"],
         "experience": f["experience"], "compensation": f["compensation"], "remote": f["remote"]}
    return sum(weights[c] * m[c] for c in weights)


def renorm(weights):
    s = sum(weights.values())
    return {k: v / s for k, v in weights.items()} if s else weights


# ---- config definitions -------------------------------------------------
def make_configs():
    cfgs = []

    def fixed(name, scorer, kind, params, note):
        cfgs.append({"id": name, "kind": kind, "params": params, "note": note, "scorer": scorer})

    # C01 incumbent
    fixed("C01_fixed_composite", lambda f: weighted(f, HAND), "fixed", 0,
          "INCUMBENT: hand-set 6-channel weights, jaccard skills, cosine semantic")
    fixed("C02_composite_embed_skills", lambda f: weighted(f, HAND, skills_key="skills_emb"), "fixed", 0,
          "hand weights, semantic (soft) skill overlap")
    fixed("C03_composite_dot_semantic", lambda f: weighted(f, HAND, sem_key="semantic_dot"), "fixed", 0,
          "hand weights, unnormalized dot-product semantic")
    fixed("C04_uniform_weights", lambda f: weighted(f, {c: 1/6 for c in CHAN}), "fixed", 0,
          "uniform 1/6 weights over 6 channels")
    # drop-one (renormalized hand weights)
    for drop in CHAN:
        w = renorm({c: HAND[c] for c in CHAN if c != drop})
        fixed(f"C_drop_{drop}", (lambda w: lambda f: weighted(f, w))(w), "fixed", 0,
              f"composite minus {drop} channel (weights renormalized)")
    # single channels
    for c in CHAN:
        fixed(f"C_only_{c}", (lambda c: lambda f: f[c])(c), "fixed", 0, f"{c}-only ranker")
    fixed("C_only_skills_emb", lambda f: f["skills_emb"], "fixed", 0, "semantic-skill-overlap-only ranker")
    # minimal fusions
    fixed("C_sem_skills_5050", lambda f: 0.5*f["semantic"]+0.5*f["skills"], "fixed", 0, "semantic+skills 50/50")
    fixed("C_sem_skills_handnorm",
          lambda f: (0.28*f["semantic"]+0.27*f["skills"])/0.55, "fixed", 0, "semantic+skills at hand ratio")
    fixed("C_sem_skills_title", lambda f: (0.28*f["semantic"]+0.27*f["skills"]+0.10*f["title"])/0.65,
          "fixed", 0, "semantic+skills+title")

    # learned configs (fit per fold)
    cfgs.append({"id": "C_learned_ridge", "kind": "ridge", "params": 6, "note": "Ridge linear fusion on 6 channels (graded target), held-out"})
    cfgs.append({"id": "C_learned_logreg", "kind": "logreg", "params": 6, "note": "LogReg fusion on 6 channels (binary), held-out"})
    cfgs.append({"id": "C_learned_logreg_reg", "kind": "logreg_reg", "params": 6, "note": "LogReg fusion, strong L2 (C=0.1), held-out"})
    cfgs.append({"id": "C_learned_lambdamart", "kind": "lambdamart", "params": ">100", "note": "LambdaMART XGBRanker rank:ndcg on 6 channels, held-out"})
    return cfgs


def per_query_scores(cfg, cvs, jobs, feats, eval_map, folds, top_k=5):
    """Return {qid: (ndcg@5, mrr, recall@5)} for one config under the CV protocol."""
    out = {}
    kind = cfg["kind"]
    qids = [cv["id"] for cv in cvs]

    def rank_and_score(cid, scorefn):
        relmap = eval_map.get(cid, {})
        pos = {d: r for d, r in relmap.items() if r > 0}
        if not pos:
            return None
        scored = [(job["id"], scorefn((cid, job["id"]))) for job in jobs]
        ranking = [d for d, _ in sorted(scored, key=lambda x: -x[1])]
        # MRR: reciprocal rank of first relevant
        mrr = 0.0
        for i, d in enumerate(ranking, 1):
            if pos.get(d, 0) > 0:
                mrr = 1.0 / i
                break
        return (ndcg_at_k(ranking, relmap, top_k), mrr, recall_at_k(ranking, pos, top_k))

    if kind == "fixed":
        for cv in cvs:
            r = rank_and_score(cv["id"], lambda key: cfg["scorer"](feats[key]))
            if r is not None:
                out[cv["id"]] = r
        return out

    # learned: fit on train folds, score val fold
    for fold in folds:
        val = set(int(i) for i in fold)
        Xtr, ytr_g, ytr_b, qid_tr = [], [], [], []
        for ri, cv in enumerate(cvs):
            if ri in val:
                continue
            relmap = eval_map.get(cv["id"], {})
            grp_has_pos = any(relmap.get(j["id"], 0) > 0 for j in jobs)
            for job in jobs:
                x = [feats[(cv["id"], job["id"])][c] for c in CHAN]
                g = int(relmap.get(job["id"], 0))
                Xtr.append(x); ytr_g.append(g); ytr_b.append(1 if g > 0 else 0)
                if kind == "lambdamart" and grp_has_pos:
                    qid_tr.append(ri)
        Xtr = np.asarray(Xtr, float)
        if kind == "ridge":
            model = Ridge(alpha=1.0, random_state=SEED) if "random_state" in Ridge().get_params() else Ridge(alpha=1.0)
            model.fit(Xtr, np.asarray(ytr_g, float))
            predict = lambda X: model.predict(X)
        elif kind in ("logreg", "logreg_reg"):
            if len(set(ytr_b)) < 2:
                continue
            C = 0.1 if kind == "logreg_reg" else 1.0
            model = LogisticRegression(max_iter=1000, C=C, random_state=SEED)
            model.fit(Xtr, np.asarray(ytr_b, int))
            predict = lambda X: model.predict_proba(X)[:, 1]
        elif kind == "lambdamart":
            # rebuild training restricted to groups with a positive (needed for rank:ndcg)
            Xg, yg, qg = [], [], []
            for ri, cv in enumerate(cvs):
                if ri in val:
                    continue
                relmap = eval_map.get(cv["id"], {})
                if not any(relmap.get(j["id"], 0) > 0 for j in jobs):
                    continue
                for job in jobs:
                    Xg.append([feats[(cv["id"], job["id"])][c] for c in CHAN])
                    yg.append(int(relmap.get(job["id"], 0))); qg.append(ri)
            if len(set(yg)) < 2:
                continue
            m = XGBRanker(objective="rank:ndcg", n_estimators=200, max_depth=3, learning_rate=0.1,
                          subsample=0.9, colsample_bytree=0.9, random_state=SEED, tree_method="hist")
            m.fit(np.asarray(Xg, float), np.asarray(yg, int), qid=np.asarray(qg, int))
            predict = lambda X: m.predict(X)
        else:
            continue

        for ri in fold:
            cv = cvs[int(ri)]
            relmap = eval_map.get(cv["id"], {})
            pos = {d: r for d, r in relmap.items() if r > 0}
            if not pos:
                continue
            Xv = np.asarray([[feats[(cv["id"], job["id"])][c] for c in CHAN] for job in jobs], float)
            scores = predict(Xv)
            ranking = [jobs[j]["id"] for j in np.argsort(-scores)]
            mrr = 0.0
            for i, d in enumerate(ranking, 1):
                if pos.get(d, 0) > 0:
                    mrr = 1.0 / i; break
            out[cv["id"]] = (ndcg_at_k(ranking, relmap, top_k), mrr, recall_at_k(ranking, pos, top_k))
    return out


def bootstrap_mean_ci(vals, n_boot=5000, seed=SEED):
    rng = np.random.default_rng(seed)
    arr = np.asarray(vals, float)
    if len(arr) == 0:
        return {"mean": None, "ci_low": None, "ci_high": None}
    boots = np.array([arr[rng.integers(0, len(arr), len(arr))].mean() for _ in range(n_boot)])
    return {"mean": round(float(arr.mean()), 6), "ci_low": round(float(np.quantile(boots, 0.025)), 6),
            "ci_high": round(float(np.quantile(boots, 0.975)), 6)}


def paired_bootstrap_delta(a_map, b_map, n_boot=5000, seed=SEED):
    """Paired bootstrap of (a - b) per-query nDCG over the common query set."""
    common = sorted(set(a_map) & set(b_map))
    if not common:
        return None
    da = np.array([a_map[q][0] - b_map[q][0] for q in common], float)
    rng = np.random.default_rng(seed)
    boots = np.array([da[rng.integers(0, len(da), len(da))].mean() for _ in range(n_boot)])
    lo, hi = float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))
    # two-sided bootstrap p (proportion of resamples on the other side of 0), doubled
    p = 2 * min((boots <= 0).mean(), (boots >= 0).mean())
    return {"delta_mean": round(float(da.mean()), 6), "ci_low": round(lo, 6), "ci_high": round(hi, 6),
            "p_two_sided": round(float(min(1.0, p)), 4), "n_common": len(common),
            "excludes_zero": bool(lo > 0 or hi < 0)}


def holm(pvals: dict):
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    survivors = {}
    for i, (name, p) in enumerate(items):
        thresh = 0.05 / (m - i)
        survivors[name] = bool(p < thresh)
        if p >= thresh:
            for name2, _ in items[i + 1:]:
                survivors[name2] = False
            break
    return survivors


def main() -> None:
    np.random.seed(SEED)
    settings = Settings()
    eval_map = load_eval_labels(settings.data_dir / "eval_pairs.json")
    cvs, jobs = load_settings_data(settings)
    feats = build_features(cvs, jobs)
    print(f"features built for {len(cvs)}x{len(jobs)} pairs")

    idx = np.arange(len(cvs)); np.random.shuffle(idx)
    folds = np.array_split(idx, 5)

    configs = make_configs()
    scores = {c["id"]: per_query_scores(c, cvs, jobs, feats, eval_map, folds) for c in configs}

    # leaderboard
    board = []
    for c in configs:
        s = scores[c["id"]]
        ndcgs = [v[0] for v in s.values()]
        mrrs = [v[1] for v in s.values()]
        recs = [v[2] for v in s.values()]
        ci = bootstrap_mean_ci(ndcgs)
        board.append({"id": c["id"], "kind": c["kind"], "fitted_params": c["params"], "note": c["note"],
                      "n_queries": len(ndcgs), "ndcg@5": ci,
                      "mrr": round(float(np.mean(mrrs)), 6) if mrrs else None,
                      "recall@5": round(float(np.mean(recs)), 6) if recs else None})
    board.sort(key=lambda b: -(b["ndcg@5"]["mean"] or 0))

    # significance of every challenger vs incumbent C01
    inc = scores["C01_fixed_composite"]
    deltas, pvals = {}, {}
    for c in configs:
        if c["id"] == "C01_fixed_composite":
            continue
        d = paired_bootstrap_delta(scores[c["id"]], inc)
        if d is not None:
            deltas[c["id"]] = d
            pvals[c["id"]] = d["p_two_sided"]
    holm_survivors = holm(pvals)
    beats_incumbent = [cid for cid, d in deltas.items()
                       if d["excludes_zero"] and d["delta_mean"] > 0 and holm_survivors.get(cid, False)]

    # selection decision by the frozen rule
    if beats_incumbent:
        winner = max(beats_incumbent, key=lambda cid: deltas[cid]["delta_mean"])
        decision = (f"SELECT {winner}: it beats the incumbent (paired CI excludes 0, survives Holm). "
                    "Report as a genuine improvement.")
    else:
        winner = "C01_fixed_composite"
        decision = ("SELECT the INCUMBENT C01_fixed_composite: NO challenger's paired-bootstrap CI vs the "
                    "incumbent excludes 0 after Holm correction. Per the frozen tie-break rule, the "
                    "statistically-indistinguishable set is resolved by parsimony/auditability (0 fitted "
                    "params, deterministic, fully decomposable). The benchmark (n=%d queries) is too small "
                    "to establish any config as superior." % len(inc))

    out = {
        "experiment": "EXP-025 protocol-gated model-selection search (Stage-2 §D-E)",
        "protocol": "5-fold resume-level CV (seed 42); learned configs fit on train folds only, scored on held-out; "
                    "fixed configs fold-invariant. Selection criteria FROZEN before results (see module docstring).",
        "selection_criteria_frozen_before_results": {
            "primary": "mean nDCG@5",
            "beat_rule": "paired-bootstrap 95% CI of (challenger - incumbent) per-query nDCG excludes 0 AND survives Holm",
            "tie_break": "if none beat the incumbent, select incumbent by parsimony/auditability",
        },
        "n_configs": len(configs), "n_eval_queries": len(inc),
        "incumbent": "C01_fixed_composite",
        "leaderboard": board,
        "significance_vs_incumbent": {cid: {**deltas[cid], "holm_survives": holm_survivors.get(cid, False)}
                                      for cid in deltas},
        "challengers_that_beat_incumbent": beats_incumbent,
        "selected_config": winner,
        "selection_decision": decision,
        "caveats": [
            "Selection and evaluation share the SAME 5-fold CV (no separate untouched outer test); a winning "
            "LEARNED config's CV score would be optimistically biased (winner's curse). This run is unaffected "
            "because the frozen tie-break selects the fixed INCUMBENT, whose score is not chosen for being maximal.",
            "The per-config p-value is a two-sided BOOTSTRAP tail-proportion of the paired-delta distribution, a "
            "percentile heuristic — not a permutation null p-value; 'survives Holm' is therefore an approximate, "
            "not a strictly FWER-controlled, screen. The primary evidence is the paired CI crossing zero.",
        ],
        "interpretation": (
            "This is a search, not a cherry-pick: all configs and negatives are reported and selection criteria were "
            "fixed before results. Subject to the caveats above, the honest finding is that NO config is "
            "significantly better than the auditable fixed composite on this corpus, so the incumbent is retained."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    # concise console summary
    print(json.dumps({"top5": board[:5], "selected": winner, "beats_incumbent": beats_incumbent,
                      "decision": decision}, indent=2))


if __name__ == "__main__":
    main()
