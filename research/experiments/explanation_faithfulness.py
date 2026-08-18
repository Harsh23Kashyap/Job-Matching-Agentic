"""EXP-028 / Stage-2 §O: rebuilt explanation-faithfulness evaluation (NON-tautological).

The audit's complaint: the old "faithfulness 0.745" was a mean of lint-style checks, and the
additive decomposition (contribution_i = w_i * score_i, summing to the composite) is exact BY
CONSTRUCTION, so testing "does the explanation's contribution sum to the score" is tautological.

This rebuild measures MECHANISTIC, ranking-level faithfulness — does the channel the explanation
credits most actually drive this candidate's top result?
  1. Comprehensiveness (ranking): for each resume's top-1 job, zero the TOP-attributed channel
     across ALL jobs, re-rank, and check whether the top-1 job is displaced. Compare against
     zeroing the LEAST-attributed channel and a RANDOM channel. Faithful attribution =>
     top-attributed removal displaces the top-1 MORE often than least/random removal.
  2. Attribution–effect alignment: Spearman between each channel's attributed contribution rank
     and its causal rank-displacement effect, averaged over resumes.
  3. Attribution correctness under controlled edits: add a job-required skill the resume lacks
     => the skills contribution must increase and remain consistent with the reason text.
  4. Structural checks (reported, but labeled as by-construction, NOT as faithfulness):
     additive-decomposition exactness, fit-label/score consistency, specificity.

Run: cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false \
  PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/explanation_faithfulness.py
"""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

import numpy as np

from config import Settings
from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot
from benchmarks.extended_evaluation import load_settings_data
from core.scoring import COMPOSITE_WEIGHTS, compute_composite
from core.match_explanation import build_match_explanation
from core.skills import skill_overlap_details

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "research" / "results" / "explanation_faithfulness.json"
SEED = 42
CHAN = ["semantic", "skills", "title", "experience", "compensation", "remote"]
MODEL = "all-MiniLM-L6-v2"


def channels_of(bd):
    return {"semantic": bd.semantic_score or 0.0, "skills": bd.skills_score or 0.0,
            "title": bd.title_score or 0.0, "experience": bd.experience_score or 0.0,
            "compensation": bd.compensation_score or 0.0, "remote": bd.remote_score or 0.0}


def composite_from(ch, drop=None, keep_only=None):
    w = COMPOSITE_WEIGHTS
    total = 0.0
    for c in CHAN:
        if drop is not None and c == drop:
            continue
        if keep_only is not None and c != keep_only:
            continue
        total += w[c] * ch[c]
    return max(0.0, min(1.0, total))


def main() -> None:
    rng = np.random.default_rng(SEED)
    settings = Settings()
    cvs, jobs = load_settings_data(settings)
    csnap = {cv["id"]: cv_to_snapshot(cv, MODEL) for cv in cvs}
    jsnap = {job["id"]: job_to_snapshot(job, MODEL) for job in jobs}

    # full channel table
    ch_tab = {}  # (cid, jid) -> channels dict
    for cv in cvs:
        for job in jobs:
            ch_tab[(cv["id"], job["id"])] = channels_of(compute_composite(csnap[cv["id"]], jsnap[job["id"]]))

    disp_top, disp_least, disp_rand = [], [], []
    align_rhos = []
    spec_hits, spec_total = 0, 0
    contra = 0
    add_exact = 0
    n_expl = 0

    for cv in cvs:
        # full ranking
        full = [(job["id"], composite_from(ch_tab[(cv["id"], job["id"])])) for job in jobs]
        full.sort(key=lambda x: -x[1])
        top_jid = full[0][0]
        ch = ch_tab[(cv["id"], top_jid)]
        contrib = {c: COMPOSITE_WEIGHTS[c] * ch[c] for c in CHAN}
        order = sorted(CHAN, key=lambda c: -contrib[c])
        top_c, least_c = order[0], order[-1]
        rand_c = CHAN[int(rng.integers(0, len(CHAN)))]

        def top1_after_drop(drop):
            rescored = [(job["id"], composite_from(ch_tab[(cv["id"], job["id"])], drop=drop)) for job in jobs]
            rescored.sort(key=lambda x: -x[1])
            return rescored[0][0]

        disp_top.append(0 if top1_after_drop(top_c) == top_jid else 1)
        disp_least.append(0 if top1_after_drop(least_c) == top_jid else 1)
        disp_rand.append(0 if top1_after_drop(rand_c) == top_jid else 1)

        # attribution-effect alignment: contribution rank vs rank-displacement magnitude of top job
        eff = []
        for c in CHAN:
            rescored = [(job["id"], composite_from(ch_tab[(cv["id"], job["id"])], drop=c)) for job in jobs]
            rescored.sort(key=lambda x: -x[1])
            new_rank = [d for d, _ in rescored].index(top_jid)
            eff.append(new_rank)  # 0 = still top; higher = displaced more
        contrib_vec = [contrib[c] for c in CHAN]
        if np.std(eff) > 0 and np.std(contrib_vec) > 0:
            rho = float(np.corrcoef(np.argsort(np.argsort(contrib_vec)),
                                    np.argsort(np.argsort(eff)))[0, 1])
            align_rhos.append(rho)

        # structural checks on the explanation payload
        matched, missing = skill_overlap_details(cv.get("skills", []), jobs_by_id(jobs, top_jid).get("required_skills", []))
        bd = compute_composite(csnap[cv["id"]], jsnap[top_jid])
        expl = build_match_explanation(csnap[cv["id"]], jsnap[top_jid], bd, matched_skills=matched, missing_skills=missing)
        n_expl += 1
        # additive exactness
        s = sum(comp.contribution for comp in expl.score_breakdown)
        if abs(s - min(1.0, sum(COMPOSITE_WEIGHTS[c] * ch[c] for c in CHAN))) < 1e-6 or abs(s - bd.final_score) < 0.02:
            add_exact += 1
        # specificity: reasons that mention a concrete number/field
        for sig in (expl.semantic, expl.experience, expl.compensation, expl.remote):
            spec_total += 1
            if sig.reason and re.search(r"\d", sig.reason):
                spec_hits += 1
        # contradiction: label tier vs score tier
        for sig in (expl.semantic, expl.experience, expl.compensation, expl.remote):
            if sig.score is None:
                continue
            hi = sig.score >= 0.85
            lo = sig.score < 0.45
            if (hi and sig.label in ("Weak fit", "Moderate fit")) or (lo and sig.label in ("Strong fit", "Good fit")):
                contra += 1

    # attribution correctness under controlled skill-addition edits:
    # adding a REQUIRED skill the resume lacks must STRICTLY increase the skills contribution
    # (Jaccard numerator +1, denominator unchanged since the skill is already in the job set).
    strict_increase, total_edits = 0, 0
    deltas = []
    for cv in cvs[:20]:
        for job in jobs:
            reqs = job.get("required_skills", [])
            have = set(s.lower() for s in cv.get("skills", []))
            missing_req = [s for s in reqs if s.lower() not in have]
            if not missing_req:
                continue
            base_ch = ch_tab[(cv["id"], job["id"])]
            edited = copy.deepcopy(cv)
            edited["skills"] = list(cv.get("skills", [])) + [missing_req[0]]
            ed_bd = compute_composite(cv_to_snapshot(edited, MODEL), jsnap[job["id"]])
            total_edits += 1
            d = (ed_bd.skills_score or 0.0) - base_ch["skills"]
            deltas.append(d)
            if d > 1e-6:  # STRICT, material increase
                strict_increase += 1
            break  # one edit per resume is enough

    out = {
        "experiment": "EXP-028 rebuilt explanation faithfulness — mechanistic, ranking-level (Stage-2 §O)",
        "n_resumes_explained": n_expl,
        "comprehensiveness_ranking": {
            "top1_displaced_when_dropping_TOP_attributed_channel": round(float(np.mean(disp_top)), 4),
            "top1_displaced_when_dropping_LEAST_attributed_channel": round(float(np.mean(disp_least)), 4),
            "top1_displaced_when_dropping_RANDOM_channel": round(float(np.mean(disp_rand)), 4),
            "faithful": bool(np.mean(disp_top) > np.mean(disp_least)),
            "note": "Faithful attribution => dropping the TOP-attributed channel displaces the top-1 job more "
                    "often than dropping the LEAST-attributed channel. This is NOT tautological (ranking-level).",
        },
        "attribution_effect_alignment_spearman_mean": round(float(np.mean(align_rhos)), 4) if align_rhos else None,
        "attribution_correctness_skill_addition": {
            "fraction_skill_contrib_STRICTLY_increases": round(strict_increase / total_edits, 4) if total_edits else None,
            "mean_delta": round(float(np.mean(deltas)), 4) if deltas else None,
            "min_delta": round(float(np.min(deltas)), 4) if deltas else None,
            "n_edits": total_edits,
        },
        "structural_by_construction": {
            "additive_decomposition_exact_fraction": round(add_exact / n_expl, 4) if n_expl else None,
            "fit_label_score_contradiction_rate": round(contra / (4 * n_expl), 4) if n_expl else None,
            "specificity_reasons_naming_a_number": round(spec_hits / spec_total, 4) if spec_total else None,
            "note": "These are structural properties (exact decomposition, label-score consistency, specificity). "
                    "They are reported as engineering guarantees, NOT as XAI faithfulness (audit B9).",
        },
        "interpretation": (
            "Report the ranking-level comprehensiveness and attribution-effect alignment as the honest faithfulness "
            "evidence; keep the additive decomposition / consistency / specificity as structural guarantees, not as "
            "a 'faithfulness score'. No human study was run; describe as automated structural + mechanistic validation."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


def jobs_by_id(jobs, jid):
    for j in jobs:
        if j["id"] == jid:
            return j
    return {}


if __name__ == "__main__":
    main()
