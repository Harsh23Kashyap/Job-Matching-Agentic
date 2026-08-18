"""EXP-043/044 / Stage-3 follow-up: graded skill channel in the LIVE scorer + a by-construction
audit of the synthetic fusion result.

Two questions, both answered under the frozen PROTOCOL.md discipline (develop on synthetic;
the real 30x15/47 corpus is a secondary transfer check touched ONCE for the frozen skill matcher):

  (A) BY-CONSTRUCTION AUDIT of EXP-035/036. The synthetic latent ground truth is
      latent = 0.40*required + 0.12*preferred + 0.15*seniority + ... where `required` and
      `preferred` are set-coverage of required/preferred skills. The +derived fusion feeds
      `required_coverage`/`preferred_coverage` straight back in. This measures how strongly the
      derived features correlate with the latent generative factors (expected ~1.0 => the +derived
      gain is largely by construction), versus the base6 channels (text/embedding-derived, NOT the
      generator). This DISCOUNTS the +derived number and identifies the honest, defensible gain
      (base6 nonlinear fusion).

  (B) GRADED SKILL CHANNEL as a genuine, frozen system improvement. Binary Jaccard gives zero
      credit to related skills and full credit only to exact matches. The graded channel
      (core.skills.graded_coverage_skills, frozen credits exact=1.0 / same-taxonomy-group=0.5)
      replaces the skill channel in the fixed composite (all other channels + weights UNCHANGED,
      no re-tuning). We report:
        * skill-channel alignment with ground truth on synthetic (correlation with clean_grade),
        * composite nDCG@5 jaccard vs graded on synthetic (paired bootstrap CI),
        * composite nDCG@5 jaccard vs graded on the REAL corpus, ONE prospective run
          (allowed by PROTOCOL.md's prospective-check rule for the newly-frozen matcher).
      Whatever the sign, it is reported honestly; on n=30 all-positive queries a "no detectable
      difference" is the expected and acceptable outcome.

Run: cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false \
  PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/graded_skill_channel.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from config import Settings
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.document_text import job_document_text, resume_document_text
from core.embedding import embed_text
from core.scoring import compute_composite, COMPOSITE_WEIGHTS
from core.skill_catalog import canonical_skill
from core.skills import jaccard_skills, graded_coverage_skills
from benchmarks.eval_data import load_eval_labels, cv_to_snapshot, job_to_snapshot
from benchmarks.extended_evaluation import load_settings_data
from benchmarks.metrics import ndcg_at_k

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "research" / "datasets" / "synthetic_v1"
OUT = REPO / "research" / "results" / "graded_skill_channel.json"
SEED = 42
MODEL = "all-MiniLM-L6-v2"


def _pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if x.std() == 0 or y.std() == 0:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def bootstrap_paired(a: dict, b: dict, n_boot=3000, seed=SEED):
    common = sorted(set(a) & set(b))
    da = np.array([a[q] - b[q] for q in common])
    rng = np.random.default_rng(seed)
    boots = np.array([da[rng.integers(0, len(da), len(da))].mean() for _ in range(n_boot)])
    lo, hi = float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))
    # Paired sign-flip permutation test (two-sided) — corroborates a marginal bootstrap CI on small n.
    obs = abs(float(da.mean()))
    prng = np.random.default_rng(seed + 7)
    n_perm = 20000
    signs = prng.integers(0, 2, size=(n_perm, len(da))) * 2 - 1
    perm_means = np.abs((signs * da).mean(axis=1))
    perm_p = float((np.sum(perm_means >= obs) + 1) / (n_perm + 1))
    return {"delta_mean": round(float(da.mean()), 5), "ci_low": round(lo, 5), "ci_high": round(hi, 5),
            "excludes_zero": bool(lo > 0 or hi < 0), "perm_p_two_sided": round(perm_p, 4),
            "n_queries": len(common)}


# ---- synthetic snapshots (reuse the fusion experiment's builders) ----
def _syn_cand(cv):
    fam = cv["job_family"].replace("_", " ")
    summary = f"{cv['title']} with {cv['experience_years']} years of {fam} experience."
    doc = resume_document_text({"skills": cv["skills"], "experience_years": cv["experience_years"],
                                "remote_preference": cv["remote_preference"], "preferred_salary": cv["preferred_salary"],
                                "summary": summary, "name": ""})
    return CandidateSnapshot(id=cv["id"], name="", skills=cv["skills"], experience_years=float(cv["experience_years"]),
                             remote_preference=bool(cv["remote_preference"]), preferred_salary=cv["preferred_salary"],
                             summary=summary, version=1, document_text_hash=hashlib.sha256(doc.encode()).hexdigest(),
                             embedding=embed_text(doc, model_name=MODEL).tolist())


def _syn_job(job):
    like = {"title": job["title"], "required_skills": job["required_skills"], "preferred_skills": job["preferred_skills"],
            "required_experience": job["required_experience_min"], "remote_policy": job["work_mode"] == "remote",
            "budget_min": job["budget_min"], "budget_max": job["budget_max"], "description": job["description"]}
    doc = job_document_text(like)
    return JobSnapshot(id=job["id"], title=like["title"], required_skills=like["required_skills"],
                       preferred_skills=like["preferred_skills"], required_experience=int(like["required_experience"]),
                       remote_policy=bool(like["remote_policy"]), budget_min=like["budget_min"], budget_max=like["budget_max"],
                       description=like["description"], version=1, document_text_hash=hashlib.sha256(doc.encode()).hexdigest(),
                       embedding=embed_text(doc, model_name=MODEL).tolist())


def by_construction_audit(resumes, jobs, labels):
    """(A) Correlate derived features + base6 channels with the stored latent generative factors."""
    lab = {(l["query_id"], l["doc_id"]): l for l in labels}
    cvmap = {r["id"]: r for r in resumes}
    jobmap = {j["id"]: j for j in jobs}
    csnap = {r["id"]: _syn_cand(r) for r in resumes}
    jsnap = {j["id"]: _syn_job(j) for j in jobs}

    req_cov, pref_cov, lat_req, lat_pref = [], [], [], []
    sem_ch, skills_ch, lat_total = [], [], []
    for (cid, jid), l in lab.items():
        cv, job = cvmap[cid], jobmap[jid]
        cs_canon = {canonical_skill(s) for s in cv["skills"]}
        rq = [canonical_skill(s) for s in job["required_skills"]]
        pf = [canonical_skill(s) for s in job["preferred_skills"]]
        req_cov.append(sum(1 for r in rq if r in cs_canon) / len(rq) if rq else 0.0)
        pref_cov.append(sum(1 for p in pf if p in cs_canon) / len(pf) if pf else 0.0)
        lat_req.append(l["latent_factors"]["required"])
        lat_pref.append(l["latent_factors"]["preferred"])
        bd = compute_composite(csnap[cid], jsnap[jid])
        sem_ch.append(bd.semantic_score or 0.0)
        skills_ch.append(bd.skills_score or 0.0)
        lat_total.append(l["latent_score"])

    return {
        "note": ("required_coverage / preferred_coverage are (up to skill canonicalization) IDENTICAL to the "
                 "latent generative factors `required` (weight 0.40) and `preferred` (weight 0.12), which "
                 "together are 0.52 of the latent score. Feeding them into the learned fusion reconstructs the "
                 "generator => the +derived nDCG gain is largely BY CONSTRUCTION and is NOT claimed as a "
                 "methodological improvement. The base6 channels are text/embedding-derived, NOT the generator."),
        "corr_required_coverage_vs_latent_required": round(_pearson(req_cov, lat_req), 4),
        "corr_preferred_coverage_vs_latent_preferred": round(_pearson(pref_cov, lat_pref), 4),
        "corr_base6_semantic_vs_latent_total": round(_pearson(sem_ch, lat_total), 4),
        "corr_base6_skills_vs_latent_total": round(_pearson(skills_ch, lat_total), 4),
        "interpretation": ("If the derived-vs-latent correlations are ~1.0 while the base6-vs-latent "
                           "correlations are much lower, the +derived fusion win is an artifact of handing the "
                           "model its own generator; the honest, defensible gain is base6 nonlinear fusion "
                           "(LambdaMART/monotonic-GBM base6 vs fixed composite in EXP-035/036)."),
    }


def _reblend_per_query(resumes_or_cvs, jids, chan, skill_of, relevance_of):
    """Re-blend the six channels with the FIXED weights, replacing only the skill channel, and return
    per-query nDCG@5. chan[(cid,jid)] holds the five non-skill channels; skill_of(cid,jid) gives the
    skill value for the variant; relevance_of(cid,jid) gives the graded relevance for the query pool."""
    w = COMPOSITE_WEIGHTS
    out = {}
    for cid in [c["id"] for c in resumes_or_cvs]:
        relmap = {}
        for jid in jids:
            if (cid, jid) not in chan:
                continue
            r = relevance_of(cid, jid)
            if r is not None:
                relmap[jid] = r
        if not any(v > 0 for v in relmap.values()):
            continue
        scores = {}
        for jid in jids:
            if (cid, jid) not in chan:
                continue
            c = chan[(cid, jid)]
            scores[jid] = max(0.0, min(1.0, w["semantic"] * c["semantic"] + w["title"] * c["title"]
                              + w["experience"] * c["experience"] + w["compensation"] * c["compensation"]
                              + w["remote"] * c["remote"] + w["skills"] * skill_of(cid, jid)))
        ranking = sorted(scores, key=lambda j: -scores[j])
        out[cid] = ndcg_at_k(ranking, relmap, 5)
    return out


def graded_channel_synthetic(resumes, jobs, labels):
    """(B) Isolate the relation-aware novelty on synthetic against clean_grade (consistent with EXP-035/036).

    THREE pre-specified skill-channel variants decompose the gain (hostile-review fix — the earlier
    jaccard-vs-graded comparison confounded the coverage FORM with the relation-aware credit):
      * jaccard          = symmetric binary set-overlap (the incumbent skill channel)
      * exact_coverage   = ASYMMETRIC binary required-coverage (graded with related_credit=0.0)
      * graded_coverage  = ASYMMETRIC coverage with relation-aware partial credit (related=0.5, the novelty)
    jaccard->exact_coverage isolates the coverage-form effect; exact_coverage->graded isolates the
    relation-aware credit (the actual contribution). Relevance target = clean_grade (matches EXP-035/036,
    so the fixed-composite baseline reconciles to 0.917)."""
    lab = {(l["query_id"], l["doc_id"]): l for l in labels}
    csnap = {r["id"]: _syn_cand(r) for r in resumes}
    jsnap = {j["id"]: _syn_job(j) for j in jobs}
    jobmap = {j["id"]: j for j in jobs}
    cvmap = {r["id"]: r for r in resumes}
    jids = [j["id"] for j in jobs]

    chan = {}
    for cv in resumes:
        for job in jobs:
            key = (cv["id"], job["id"])
            if key not in lab:
                continue
            bd = compute_composite(csnap[cv["id"]], jsnap[job["id"]], skills_mode="jaccard")
            chan[key] = {"semantic": bd.semantic_score or 0.0, "title": bd.title_score or 0.0,
                         "experience": bd.experience_score or 0.0, "compensation": bd.compensation_score or 0.0,
                         "remote": bd.remote_score or 0.0}

    rel_of = lambda cid, jid: lab[(cid, jid)]["clean_grade"]
    jac_of = lambda cid, jid: jaccard_skills(cvmap[cid]["skills"], jobmap[jid]["required_skills"])
    cov_of = lambda credit: (lambda cid, jid: graded_coverage_skills(
        cvmap[cid]["skills"], jobmap[jid]["required_skills"], related_credit=credit))

    jac_q = _reblend_per_query(resumes, jids, chan, jac_of, rel_of)
    exact_q = _reblend_per_query(resumes, jids, chan, cov_of(0.0), rel_of)
    grad_q = _reblend_per_query(resumes, jids, chan, cov_of(0.5), rel_of)

    sweep = {}
    for credit in (0.0, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7):
        gq = _reblend_per_query(resumes, jids, chan, cov_of(credit), rel_of)
        sweep[str(credit)] = {"ndcg5": round(float(np.mean(list(gq.values()))), 5),
                              "vs_jaccard": bootstrap_paired(gq, jac_q)["delta_mean"]}

    return {
        "relevance_target": "clean_grade (matches EXP-035/036; reconciles the fixed-composite baseline)",
        "composite_ndcg5": {
            "jaccard_symmetric": round(float(np.mean(list(jac_q.values()))), 5),
            "exact_coverage_asymmetric": round(float(np.mean(list(exact_q.values()))), 5),
            "graded_coverage_asymmetric": round(float(np.mean(list(grad_q.values()))), 5),
        },
        "gain_decomposition": {
            "coverage_form_effect_exact_vs_jaccard": bootstrap_paired(exact_q, jac_q),
            "relation_aware_effect_graded_vs_exact": bootstrap_paired(grad_q, exact_q),
            "total_graded_vs_jaccard": bootstrap_paired(grad_q, jac_q),
        },
        "credit_weight_sweep": sweep,
        "n_queries": len(jac_q),
    }


def graded_channel_real():
    """(B) Real corpus: THREE PRE-SPECIFIED frozen skill-channel variants (no parameter selected on the
    test corpus), isolating the relation-aware novelty from the coverage-form change.

      * jaccard         = symmetric binary set-overlap (incumbent)
      * exact_coverage  = asymmetric binary required-coverage (graded, related_credit=0.0)   [frozen]
      * graded_coverage = asymmetric coverage + relation-aware partial credit (0.5)           [frozen]
    All three are pre-specified a priori; the related=0.5 credit is the frozen EXP-034 value. No
    credit-weight sweep is run on the real corpus (that sweep lives on synthetic dev only), so this
    honours 'one prospective evaluation, no test-corpus tuning'. We report the gain decomposition and a
    per-query breakdown for the novelty step (graded vs exact_coverage)."""
    settings = Settings()
    eval_map = load_eval_labels(settings.data_dir / "eval_pairs.json")
    cvs, jobs = load_settings_data(settings)
    csnap = {cv["id"]: cv_to_snapshot(cv, MODEL) for cv in cvs}
    jsnap = {job["id"]: job_to_snapshot(job, MODEL) for job in jobs}
    cvmap = {cv["id"]: cv for cv in cvs}
    jobmap = {job["id"]: job for job in jobs}
    jids = [job["id"] for job in jobs]

    chan = {}
    for cv in cvs:
        for job in jobs:
            bd = compute_composite(csnap[cv["id"]], jsnap[job["id"]], skills_mode="jaccard")
            chan[(cv["id"], job["id"])] = {
                "semantic": bd.semantic_score or 0.0, "title": bd.title_score or 0.0,
                "experience": bd.experience_score or 0.0, "compensation": bd.compensation_score or 0.0,
                "remote": bd.remote_score or 0.0, "_jac": bd.skills_score or 0.0}

    rel_of = lambda cid, jid: eval_map.get(cid, {}).get(jid)
    jac_of = lambda cid, jid: chan[(cid, jid)]["_jac"]
    cov_of = lambda credit: (lambda cid, jid: graded_coverage_skills(
        cvmap[cid].get("skills", []), jobmap[jid].get("required_skills", []), related_credit=credit))

    jac_q = _reblend_per_query(cvs, jids, chan, jac_of, rel_of)
    exact_q = _reblend_per_query(cvs, jids, chan, cov_of(0.0), rel_of)
    grad_q = _reblend_per_query(cvs, jids, chan, cov_of(0.5), rel_of)

    # per-query decomposition of the NOVELTY step (graded vs exact_coverage) and total (graded vs jaccard)
    def decomp(a, b):
        common = sorted(set(a) & set(b))
        deltas = sorted(((a[q] - b[q], q) for q in common), reverse=True)
        return {"queries_improved": sum(1 for d, _ in deltas if d > 1e-9),
                "queries_worsened": sum(1 for d, _ in deltas if d < -1e-9),
                "queries_unchanged": sum(1 for d, _ in deltas if abs(d) <= 1e-9),
                "top3_deltas": [(round(d, 4), q) for d, q in deltas[:3]]}

    return {
        "protocol": "THREE pre-specified frozen variants; NO parameter selected on the real corpus; "
                    "weights UNCHANGED. No credit-weight sweep on the real corpus (synthetic-dev only).",
        "n_queries": len(jac_q),
        "composite_ndcg5": {
            "jaccard_symmetric": round(float(np.mean(list(jac_q.values()))), 5),
            "exact_coverage_asymmetric": round(float(np.mean(list(exact_q.values()))), 5),
            "graded_coverage_asymmetric": round(float(np.mean(list(grad_q.values()))), 5),
        },
        "gain_decomposition": {
            "coverage_form_effect_exact_vs_jaccard": bootstrap_paired(exact_q, jac_q),
            "relation_aware_effect_graded_vs_exact": bootstrap_paired(grad_q, exact_q),
            "total_graded_vs_jaccard": bootstrap_paired(grad_q, jac_q),
        },
        "per_query": {"graded_vs_exact_coverage": decomp(grad_q, exact_q),
                      "graded_vs_jaccard": decomp(grad_q, jac_q)},
    }


def main() -> None:
    resumes = json.loads((DATA / "synthetic_resumes.json").read_text())
    jobs = json.loads((DATA / "synthetic_jobs.json").read_text())
    labels = json.loads((DATA / "synthetic_relevance.json").read_text())["labels"]
    print(f"synthetic: {len(resumes)} resumes x {len(jobs)} jobs, {len(labels)} labels")

    audit = by_construction_audit(resumes, jobs, labels)
    syn = graded_channel_synthetic(resumes, jobs, labels)
    real = graded_channel_real()

    out = {
        "experiment": "EXP-043 graded skill channel (live scorer) + EXP-044 by-construction audit of synthetic fusion",
        "governing_rule": "MAXIMUM SCIENTIFIC CREDIBILITY, not maximum metric. Frozen rules; weights unchanged; "
                          "real corpus touched ONCE (prospective-check rule). All signs reported honestly.",
        "A_by_construction_audit": audit,
        "B_graded_skill_channel_synthetic": syn,
        "B_graded_skill_channel_real_prospective": real,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
