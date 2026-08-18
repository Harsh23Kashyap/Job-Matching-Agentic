"""Side-by-side sample of the three explanation conditions for ONE job's shortlist — a single
self-contained HTML to show a supervisor/reviewer what the human study (Goal 5) compares.

The SAME ranking (same 5 candidates, same order) is shown three ways; only the explanation differs:
  A. Score only            B. Generic template            C. Factor-grounded (JobMatch)
This makes the contribution visible: A/B are controls; C exposes the six-channel decomposition and the
matched/missing required skills that drive the rank.

Run: cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false PYTHONHASHSEED=0 \
  PYTHONPATH=. .venv/bin/python ../research/experiments/make_sidebyside_sample.py [job_id]
"""
from __future__ import annotations

import html
import sys
from pathlib import Path

from config import Settings
import json
from core.scoring import compute_composite
from core.skills import skill_overlap_details
from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "research" / "datasets" / "explanation_study" / "SIDE_BY_SIDE_sample.html"
MODEL = "all-MiniLM-L6-v2"
TOP_K = 5
CH = {"semantic": "Semantic", "skills": "Skills", "title": "Title", "experience": "Experience",
      "compensation": "Compensation", "remote": "Remote"}

CSS = ("body{font:13px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;margin:20px;color:#111}"
       "h1{font-size:18px}h2{font-size:14px;margin:0 0 8px}.note{color:#555;max-width:1100px}"
       ".grid{display:flex;gap:14px;align-items:flex-start}.col{flex:1;border:1px solid #dde;border-radius:8px;padding:10px 12px;background:#fafbfc}"
       ".cond{font-weight:700;color:#036;border-bottom:2px solid #cde;padding-bottom:4px;margin-bottom:8px}"
       ".cand{border:1px solid #e3e3e3;border-radius:6px;padding:8px 10px;margin:8px 0;background:#fff}"
       ".rank{color:#666;font-weight:700}.score{color:#0a7;font-weight:700}"
       ".bar{display:inline-block;height:8px;background:#8ac;border-radius:3px;vertical-align:middle}"
       ".m{color:#0a7}.x{color:#c33}table{border-collapse:collapse;font-size:12px;margin-top:4px}td{padding:0 6px 0 0}"
       ".job{background:#eef3f8;border:1px solid #cdd;padding:8px 12px;border-radius:8px;margin:10px 0}")


def conf(s):
    return f"{round(100*s)}% ({'High' if s>=0.66 else 'Medium' if s>=0.4 else 'Low'})"


def card(cond, rank, cv, job, bd):
    name = html.escape(cv.get("name", cv["id"]))
    head = f'<div class="cand"><span class="rank">#{rank}</span> <b>{name}</b> &middot; <span class="score">{bd.final_score:.2f}</span>'
    if cond == "A":
        return head + "</div>"
    if cond == "B":
        return head + '<div>This candidate is a strong overall match for the role.</div></div>'
    rows = "".join(
        f'<tr><td>{CH.get(c.key,c.label)}</td><td>{c.weight:.2f}&times;{c.score:.2f}</td>'
        f'<td><span class="bar" style="width:{int(round(70*max(0,min(1,c.score))))}px"></span> {c.contribution:.3f}</td></tr>'
        for c in (bd.score_components or []))
    matched, missing = skill_overlap_details(cv.get("skills", []), job.get("required_skills", []))
    return (head + f'<div>Confidence: {conf(bd.final_score)}</div><table>{rows}</table>'
            f'<div class="m">Matched: {html.escape(", ".join(matched) or "none")}</div>'
            f'<div class="x">Missing: {html.escape(", ".join(missing) or "none")}</div></div>')


def main():
    settings = Settings()
    jid = sys.argv[1] if len(sys.argv) > 1 else "job_01"
    cvs = json.loads((settings.data_dir / "cvs.json").read_text())
    jobs = {j["id"]: j for j in json.loads((settings.data_dir / "jobs.json").read_text())}
    job = jobs[jid]
    csnap = {cv["id"]: cv_to_snapshot(cv, MODEL) for cv in cvs}
    jsn = job_to_snapshot(job, MODEL)
    scored = sorted(((cv, compute_composite(csnap[cv["id"]], jsn)) for cv in cvs), key=lambda t: -t[1].final_score)[:TOP_K]

    cols = ""
    for code, title in (("A", "A. Score only (control)"), ("B", "B. Generic template (control)"),
                        ("C", "C. Factor-grounded (JobMatch)")):
        cards = "".join(card(code, i + 1, cv, job, bd) for i, (cv, bd) in enumerate(scored))
        cols += f'<div class="col"><div class="cond">{title}</div>{cards}</div>'

    doc = (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style>"
           f"<title>Explanation conditions — {jid}</title></head><body>"
           f"<h1>What the human study compares (one shortlist, three explanation conditions)</h1>"
           f'<p class="note">The <b>ranking is identical</b> across all three columns; only the explanation '
           f"differs. Columns A and B are controls; column C is JobMatch's factor-grounded explanation "
           f"(six-channel decomposition = weight&times;score contribution, plus matched/missing required "
           f"skills and a confidence band). The study measures whether C improves recruiters' decision "
           f"quality, speed, appropriate trust, and their ability to name why a candidate ranked where it did.</p>"
           f'<div class="job"><b>Open role:</b> {html.escape(job.get("title", jid))} &nbsp; '
           f'<b>Required skills:</b> {html.escape(", ".join(job.get("required_skills", [])))}</div>'
           f'<div class="grid">{cols}</div></body></html>')
    OUT.write_text(doc, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}  (job {jid}: {job.get('title','')}, top-{TOP_K} shortlist x 3 conditions)")


if __name__ == "__main__":
    main()
