"""EXP-035/036 / Stage-3 P2+P3: derived skill features + fusion-model comparison on the synthetic corpus.

Question (methodology improvement, developed on SYNTHETIC per PROTOCOL.md; real corpus stays untouched
test): do (a) derived skill features (required/preferred coverage, skill deficit, graded skill-semantics
credit) and (b) stronger fusion models (ridge / logistic / LambdaMART / monotonic-GBM) MATERIALLY improve
ranking over the fixed 6-channel composite? Selection by the frozen criteria (5-fold resume CV nDCG@5;
a challenger only "wins" if its paired-bootstrap CI vs the fixed composite excludes 0; ties → prefer the
simpler/more auditable model). All models + both feature sets reported; negatives preserved.

Feature sets:
  base6   = [semantic, skills, title, experience, compensation, remote]  (the composite channels)
  +derived= base6 + [required_coverage, preferred_coverage, skill_deficit_frac, graded_skill_coverage,
                     experience_deficit, experience_excess]
Models: fixed_composite (hand weights, reference) · ridge · logreg · lambdamart · monotonic_gbm.
Graded skill coverage uses the EXP-034 relation classes (exact 1.0 / taxonomy-related 0.5 / else 0.0).

Run: cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false \
  PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/synthetic/feature_fusion_synth.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import Ridge, LogisticRegression
from xgboost import XGBRanker, XGBRegressor

from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.document_text import job_document_text, resume_document_text
from core.embedding import embed_text
from core.scoring import compute_composite, COMPOSITE_WEIGHTS
from core.skill_catalog import canonical_skill
from core.skill_taxonomy import skill_groups
from benchmarks.metrics import ndcg_at_k

import os
REPO = Path(__file__).resolve().parents[3]
_SYNTH = os.environ.get("SYNTH_VERSION", "synthetic_v1")  # backward-compatible default
DATA = REPO / "research" / "datasets" / _SYNTH
OUT = REPO / "research" / "results" / ("feature_fusion_synth.json" if _SYNTH == "synthetic_v1"
                                       else f"feature_fusion_{_SYNTH}.json")
SEED = 42
MODEL = "all-MiniLM-L6-v2"
BASE6 = ["semantic", "skills", "title", "experience", "compensation", "remote"]
DERIVED = ["required_coverage", "preferred_coverage", "skill_deficit_frac", "graded_skill_coverage",
           "experience_deficit", "experience_excess"]


def _cand(cv):
    fam = cv["job_family"].replace("_", " ")
    like = {"skills": cv["skills"], "experience_years": cv["experience_years"],
            "remote_preference": cv["remote_preference"], "preferred_salary": cv["preferred_salary"],
            "summary": f"{cv['title']} with {cv['experience_years']} years of {fam} experience."}
    doc = resume_document_text({**like, "name": ""})
    return CandidateSnapshot(id=cv["id"], name="", skills=like["skills"], experience_years=float(like["experience_years"]),
                             remote_preference=bool(like["remote_preference"]), preferred_salary=like["preferred_salary"],
                             summary=like["summary"], version=1, document_text_hash=hashlib.sha256(doc.encode()).hexdigest(),
                             embedding=embed_text(doc, model_name=MODEL).tolist())


def _job(job):
    like = {"title": job["title"], "required_skills": job["required_skills"], "preferred_skills": job["preferred_skills"],
            "required_experience": job["required_experience_min"], "remote_policy": job["work_mode"] == "remote",
            "budget_min": job["budget_min"], "budget_max": job["budget_max"], "description": job["description"]}
    doc = job_document_text(like)
    return JobSnapshot(id=job["id"], title=like["title"], required_skills=like["required_skills"],
                       preferred_skills=like["preferred_skills"], required_experience=int(like["required_experience"]),
                       remote_policy=bool(like["remote_policy"]), budget_min=like["budget_min"], budget_max=like["budget_max"],
                       description=like["description"], version=1, document_text_hash=hashlib.sha256(doc.encode()).hexdigest(),
                       embedding=embed_text(doc, model_name=MODEL).tolist())


def _graded_credit(cv_skill, job_skill):
    if canonical_skill(cv_skill) == canonical_skill(job_skill):
        return 1.0
    ga, gb = skill_groups([cv_skill]), skill_groups([job_skill])
    return 0.5 if (ga and gb and (ga & gb)) else 0.0


def derived_features(cv, job):
    cs = [s for s in cv["skills"]]
    req = job["required_skills"]; pref = job["preferred_skills"]
    cs_canon = {canonical_skill(s) for s in cs}
    req_canon = [canonical_skill(s) for s in req]
    pref_canon = [canonical_skill(s) for s in pref]
    req_cov = sum(1 for r in req_canon if r in cs_canon) / len(req_canon) if req_canon else 0.0
    pref_cov = sum(1 for p in pref_canon if p in cs_canon) / len(pref_canon) if pref_canon else 0.0
    deficit = sum(1 for r in req_canon if r not in cs_canon) / len(req_canon) if req_canon else 0.0
    graded = (sum(max((_graded_credit(s, r) for s in cs), default=0.0) for r in req) / len(req)) if req else 0.0
    lo = job["required_experience_min"]
    exp_def = max(0.0, lo - cv["experience_years"]) / 10.0
    exp_exc = max(0.0, cv["experience_years"] - job["required_experience_max"]) / 10.0
    return [req_cov, pref_cov, deficit, graded, exp_def, exp_exc]


def bootstrap_paired(a, b, n_boot=3000, seed=SEED):
    common = sorted(set(a) & set(b))
    da = np.array([a[q] - b[q] for q in common])
    rng = np.random.default_rng(seed)
    boots = np.array([da[rng.integers(0, len(da), len(da))].mean() for _ in range(n_boot)])
    lo, hi = float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))
    return {"delta_mean": round(float(da.mean()), 5), "ci_low": round(lo, 5), "ci_high": round(hi, 5),
            "excludes_zero": bool(lo > 0 or hi < 0)}


def main() -> None:
    rng = np.random.default_rng(SEED)
    resumes = json.loads((DATA / "synthetic_resumes.json").read_text())
    jobs = json.loads((DATA / "synthetic_jobs.json").read_text())
    labels = json.loads((DATA / "synthetic_relevance.json").read_text())["labels"]
    lab = {(l["query_id"], l["doc_id"]): l for l in labels}
    cand = {r["id"]: _cand(r) for r in resumes}
    jsn = {j["id"]: _job(j) for j in jobs}
    jobmap = {j["id"]: j for j in jobs}; cvmap = {r["id"]: r for r in resumes}
    print(f"embedded {len(cand)} resumes + {len(jsn)} jobs")

    # feature table per (cid, jid)
    feat, grade, comp_score = {}, {}, {}
    for cv in resumes:
        for job in jobs:
            key = (cv["id"], job["id"])
            if key not in lab:
                continue
            bd = compute_composite(cand[cv["id"]], jsn[job["id"]])
            ch = [bd.semantic_score or 0, bd.skills_score or 0, bd.title_score or 0,
                  bd.experience_score or 0, bd.compensation_score or 0, bd.remote_score or 0]
            feat[key] = ch + derived_features(cvmap[cv["id"]], jobmap[job["id"]])
            grade[key] = lab[key]["clean_grade"]
            comp_score[key] = bd.final_score

    ridx = np.arange(len(resumes)); rng.shuffle(ridx)
    folds = np.array_split(ridx, 5)
    jids = [j["id"] for j in jobs]

    def per_query_ndcg_fixed():
        out = {}
        for cv in resumes:
            relmap = {jid: grade[(cv["id"], jid)] for jid in jids if (cv["id"], jid) in grade}
            if not any(v > 0 for v in relmap.values()):
                continue
            ranking = [jid for jid in sorted(relmap, key=lambda jid: -comp_score[(cv["id"], jid)])]
            out[cv["id"]] = ndcg_at_k(ranking, relmap, 5)
        return out

    def per_query_ndcg_learned(kind, cols):
        out = {}
        for fold in folds:
            val = set(int(i) for i in fold)
            tr_keys = [(resumes[ri]["id"], jid) for ri in range(len(resumes)) if ri not in val for jid in jids
                       if (resumes[ri]["id"], jid) in feat]
            X = np.array([[feat[k][c] for c in cols] for k in tr_keys])
            yg = np.array([grade[k] for k in tr_keys])
            if kind == "ridge":
                m = Ridge(alpha=1.0).fit(X, yg.astype(float)); pred = lambda Z: m.predict(Z)
            elif kind == "logreg":
                yb = (yg > 0).astype(int)
                if len(set(yb)) < 2: continue
                m = LogisticRegression(max_iter=1000, C=1.0, random_state=SEED).fit(X, yb); pred = lambda Z: m.predict_proba(Z)[:, 1]
            elif kind in ("lambdamart", "monotonic_gbm"):
                grp, Xg, yg2 = [], [], []
                for ri in range(len(resumes)):
                    if ri in val: continue
                    cid = resumes[ri]["id"]
                    ks = [(cid, jid) for jid in jids if (cid, jid) in feat]
                    if not any(grade[k] > 0 for k in ks): continue
                    for k in ks: Xg.append([feat[k][c] for c in cols]); yg2.append(grade[k]); grp.append(ri)
                if len(set(yg2)) < 2: continue
                if kind == "lambdamart":
                    m = XGBRanker(objective="rank:ndcg", n_estimators=150, max_depth=3, learning_rate=0.1,
                                  subsample=0.9, colsample_bytree=0.9, random_state=SEED, tree_method="hist")
                    m.fit(np.asarray(Xg, float), np.asarray(yg2, int), qid=np.asarray(grp, int)); pred = lambda Z: m.predict(Z)
                else:
                    mono = tuple([1] * len(cols))  # monotone increasing in every (higher feature => not-worse)
                    m = XGBRegressor(n_estimators=150, max_depth=3, learning_rate=0.1, subsample=0.9,
                                     colsample_bytree=0.9, random_state=SEED, tree_method="hist",
                                     monotone_constraints=mono)
                    m.fit(np.asarray(Xg, float), np.asarray(yg2, float)); pred = lambda Z: m.predict(Z)
            for ri in fold:
                cid = resumes[int(ri)]["id"]
                relmap = {jid: grade[(cid, jid)] for jid in jids if (cid, jid) in grade}
                if not any(v > 0 for v in relmap.values()): continue
                Z = np.array([[feat[(cid, jid)][c] for c in cols] for jid in jids if (cid, jid) in feat])
                order_jids = [jid for jid in jids if (cid, jid) in feat]
                scores = pred(Z)
                ranking = [order_jids[i] for i in np.argsort(-scores)]
                out[cid] = ndcg_at_k(ranking, relmap, 5)
        return out

    base_cols = list(range(6))
    all_cols = list(range(6 + len(DERIVED)))
    pref_idx = 6 + DERIVED.index("preferred_coverage")  # synthetic-only feature (real corpus lacks it)
    nopref_cols = [c for c in all_cols if c != pref_idx]
    results = {}
    results["fixed_composite"] = per_query_ndcg_fixed()
    for kind in ("ridge", "logreg", "lambdamart", "monotonic_gbm"):
        results[f"{kind}__base6"] = per_query_ndcg_learned(kind, base_cols)
        results[f"{kind}__+derived"] = per_query_ndcg_learned(kind, all_cols)
    # ablation: derived WITHOUT the non-transferable preferred_coverage feature (panel: real corpus has none)
    for kind in ("lambdamart", "monotonic_gbm"):
        results[f"{kind}__+derived_no_pref"] = per_query_ndcg_learned(kind, nopref_cols)

    fixed = results["fixed_composite"]
    table = {}
    for name, d in results.items():
        vals = list(d.values())
        table[name] = {"ndcg@5_mean": round(float(np.mean(vals)), 5), "n": len(vals)}
        if name != "fixed_composite":
            table[name]["vs_fixed"] = bootstrap_paired(d, fixed)

    beats = [n for n, t in table.items() if n != "fixed_composite" and t.get("vs_fixed", {}).get("excludes_zero")
             and t["vs_fixed"]["delta_mean"] > 0]
    ranked = sorted(table.items(), key=lambda kv: -kv[1]["ndcg@5_mean"])

    out = {
        "experiment": "EXP-035/036 derived features + fusion-model comparison on synthetic (Stage-3 P2/P3)",
        "protocol": "synthetic development/validation ONLY (real corpus is untouched test); 5-fold resume CV; "
                    "selection frozen in PROTOCOL.md; all models + both feature sets reported; negatives preserved",
        "feature_sets": {"base6": BASE6, "+derived": BASE6 + DERIVED},
        "leaderboard": [{"model": n, **t} for n, t in ranked],
        "challengers_beating_fixed_composite_CI_excl_0": beats,
        "interpretation": (
            "On the SYNTHETIC corpus (where there is statistical power), report whether derived skill features "
            "and/or learned fusion beat the fixed composite (paired CI excludes 0). This is development/validation "
            "evidence; the real 30x15 corpus remains the untouched test. If nothing beats the fixed composite, "
            "that parity is the honest finding and the auditable composite is retained by the frozen tie-break."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps({"leaderboard": out["leaderboard"], "beats_fixed": beats}, indent=2))


if __name__ == "__main__":
    main()
