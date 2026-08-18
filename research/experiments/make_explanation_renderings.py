"""Explanation-rendering engine (Goal-5 stimulus generator, per supervisor feedback 2026-08-18).

Generates the THREE explanation conditions the eventual blinded human study compares, for the frozen
corpus, straight from the live scorer — so the "explainable" contribution has concrete, reproducible
study stimuli. Reusable and deterministic; renders nothing fabricated.

Task unit = one JOB and its top-5 ranked candidates (the recruiter "shortlist screen"). For each screen
we render the same ranking under three explanation conditions:
  A. score-only        : rank + composite score only (control: no explanation).
  B. generic-template  : rank + a fixed generic sentence (control: any text vs none).
  C. factor-grounded   : rank + the six-channel decomposition (weight x score = contribution) +
                         matched / missing required skills + confidence (JobMatch's explanation).
Layout/length are held equal across conditions (only the explanation text differs), per the protocol.

Output: research/datasets/explanation_study/  (one self-contained .html per job x condition + manifest.csv
+ INSTRUMENT.md). Items are tagged with whether the shortlist contains any labeled-relevant candidate,
so the study can later stratify (proper system-correct / system-wrong items need the G2 explicit negatives).

Run: cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false PYTHONHASHSEED=0 \
  PYTHONPATH=. .venv/bin/python ../research/experiments/make_explanation_renderings.py
"""
from __future__ import annotations

import csv
import html
import json
from pathlib import Path

from config import Settings
from core.scoring import compute_composite
from core.skills import skill_overlap_details
from benchmarks.eval_data import load_eval_labels, cv_to_snapshot, job_to_snapshot

REPO = Path(__file__).resolve().parents[2]
OUTDIR = REPO / "research" / "datasets" / "explanation_study"
MODEL = "all-MiniLM-L6-v2"
TOP_K = 5
CONDITIONS = ("score_only", "generic_template", "factor_grounded")

_CSS = ("body{font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;max-width:820px;margin:24px auto;color:#111}"
        ".job{background:#f5f7fa;border:1px solid #dde;padding:12px 16px;border-radius:8px;margin-bottom:16px}"
        ".cand{border:1px solid #e2e2e2;border-radius:8px;padding:12px 16px;margin:10px 0}"
        ".rank{color:#555;font-weight:600}.score{color:#0a7;font-weight:600}"
        ".bar{display:inline-block;height:9px;background:#8ac;border-radius:3px;vertical-align:middle}"
        ".chan{font-size:13px;color:#333;margin:2px 0}.match{color:#0a7}.miss{color:#c33}"
        "table{border-collapse:collapse;font-size:13px;margin-top:6px}td{padding:1px 8px 1px 0}"
        "h2{font-size:16px;margin:18px 0 6px}.q{background:#fffbe6;border:1px solid #eebb;padding:8px 12px;border-radius:6px;margin-top:14px}")

_CHANNEL_LABELS = {"semantic": "Semantic fit", "skills": "Skills coverage", "title": "Title fit",
                   "experience": "Experience", "compensation": "Compensation", "remote": "Remote fit"}


def _fmt_conf(score: float) -> str:
    band = "High" if score >= 0.66 else ("Medium" if score >= 0.4 else "Low")
    return f"{round(100 * score)}% ({band})"


def _render_candidate(cond: str, rank: int, cv: dict, job: dict, bd) -> str:
    name = html.escape(cv.get("name", cv["id"]))
    score = bd.final_score
    head = f'<div class="cand"><span class="rank">#{rank}</span> &nbsp;<b>{name}</b> &nbsp;<span class="score">score {score:.2f}</span>'
    if cond == "score_only":
        return head + "</div>"
    if cond == "generic_template":
        return head + '<div class="chan">This candidate is a strong overall match for the role.</div></div>'
    # factor_grounded
    rows = []
    for comp in (bd.score_components or []):
        w = comp.weight; s = comp.score; contrib = comp.contribution
        barw = int(round(120 * max(0.0, min(1.0, s))))
        rows.append(f'<tr><td>{html.escape(_CHANNEL_LABELS.get(comp.key, comp.label))}</td>'
                    f'<td>weight {w:.2f}</td><td>score {s:.2f}</td>'
                    f'<td><span class="bar" style="width:{barw}px"></span> {contrib:.3f}</td></tr>')
    matched, missing = skill_overlap_details(cv.get("skills", []), job.get("required_skills", []))
    ms = ('<div class="chan match">Matched skills: ' + html.escape(", ".join(matched) or "none") + "</div>"
          '<div class="chan miss">Missing required: ' + html.escape(", ".join(missing) or "none") + "</div>")
    return (head + f'<div class="chan">Confidence: {_fmt_conf(score)}</div>'
            + "<table>" + "".join(rows) + "</table>" + ms + "</div>")


def _instrument_block() -> str:
    return ('<div class="q"><b>For this screen:</b><br>'
            "1. Which candidates would you advance? (check)<br>"
            "2. How confident are you in your decision? (1-7)<br>"
            "3. How useful was the information shown for deciding? (1-7)<br>"
            "4. Which single factor most drove the top candidate's rank? (free text)<br>"
            "5. How much do you trust this ranking? (1-7)</div>")


def main() -> None:
    settings = Settings()
    cvs = json.loads((settings.data_dir / "cvs.json").read_text())
    jobs = json.loads((settings.data_dir / "jobs.json").read_text())
    eval_map = load_eval_labels(settings.data_dir / "eval_pairs.json")
    csnap = {cv["id"]: cv_to_snapshot(cv, MODEL) for cv in cvs}
    jsnap = {job["id"]: job_to_snapshot(job, MODEL) for job in jobs}
    cvmap = {cv["id"]: cv for cv in cvs}

    OUTDIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for job in jobs:
        jid = job["id"]
        scored = [(cv["id"], compute_composite(csnap[cv["id"]], jsnap[jid])) for cv in cvs]
        scored.sort(key=lambda t: -t[1].final_score)
        top = scored[:TOP_K]
        # relevant candidates for this job (candidate->job labels): rel>=1
        rel_here = {cid for cid, rel in ((cv["id"], eval_map.get(cv["id"], {}).get(jid, 0)) for cv in cvs) if rel >= 1}
        shortlist_has_relevant = any(cid in rel_here for cid, _ in top)
        jtitle = html.escape(job.get("title", jid))
        jreq = html.escape(", ".join(job.get("required_skills", [])))
        for cond in CONDITIONS:
            cards = "".join(_render_candidate(cond, i + 1, cvmap[cid], job, bd)
                            for i, (cid, bd) in enumerate(top))
            doc = (f"<!doctype html><html><head><meta charset='utf-8'><style>{_CSS}</style>"
                   f"<title>{jid} — {cond}</title></head><body>"
                   f'<div class="job"><b>Open role:</b> {jtitle}<br><b>Required skills:</b> {jreq}<br>'
                   f'<b>Condition:</b> {cond}</div>'
                   f"<h2>Ranked candidates</h2>{cards}{_instrument_block()}</body></html>")
            fn = f"{jid}__{cond}.html"
            (OUTDIR / fn).write_text(doc, encoding="utf-8")
            manifest.append({"file": fn, "job_id": jid, "condition": cond, "n_candidates": len(top),
                             "shortlist_has_labeled_relevant": shortlist_has_relevant,
                             "top1_candidate": top[0][0] if top else "", "top1_score": round(top[0][1].final_score, 4) if top else ""})

    with (OUTDIR / "manifest.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(manifest[0].keys())); w.writeheader(); w.writerows(manifest)

    (OUTDIR / "INSTRUMENT.md").write_text(
        "# Explanation study — instrument (template; adjust per IRB/design)\n\n"
        "Between-subjects factor = CONDITION {score_only, generic_template, factor_grounded}; each participant "
        "sees one condition across all screens (`*__<condition>.html`). Per screen, collect: advance decision "
        "(vs the reference labels), decision confidence (1-7), information usefulness (1-7), perceived top "
        "factor (free text -> compare to the model's top channel for faithfulness), trust (1-7); log time-to-"
        "decision. Analyse with a mixed-effects model (outcome ~ condition + (1|participant) + (1|screen)); "
        "Holm across the pre-registered families. See docs/submission/eswa/HUMAN_STUDY_PROTOCOL.md.\n\n"
        "NOTE: valid *system-wrong* items (needed for the trust-calibration test) require the G2 explicit "
        "negatives; until then `shortlist_has_labeled_relevant` in manifest.csv is only a coarse proxy.\n",
        encoding="utf-8")

    n_html = len(manifest)
    print(f"wrote {n_html} stimulus screens ({len(jobs)} jobs x {len(CONDITIONS)} conditions) + manifest.csv "
          f"+ INSTRUMENT.md to {OUTDIR.relative_to(REPO)}")
    print(f"conditions: {CONDITIONS}; top-{TOP_K} candidates per screen; "
          f"screens whose shortlist contains a labeled-relevant candidate: "
          f"{sum(1 for m in manifest if m['shortlist_has_labeled_relevant']) // len(CONDITIONS)}/{len(jobs)}")


if __name__ == "__main__":
    main()
