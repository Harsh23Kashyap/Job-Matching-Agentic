"""Generate a ready-to-annotate sheet for the CURRENTLY-UNJUDGED (resume, job) pairs in the frozen
real corpus, to convert the closed-world "assumed grade-0" pairs into EXPLICITLY-judged labels.

Why: the sharpest reviewer objection is that the 47 labels are exclusively positive and the other
403 of the 30x15=450 pairs are only assumed irrelevant (closed-world). Getting those explicitly
judged yields the explicitly-negative-judged benchmark reviewers asked for, WITHOUT new resumes/jobs
(it uses the existing committed corpus). This script fabricates NOTHING: the grade columns are blank
for two human annotators + an adjudicator to fill, exactly as BENCHMARK_ANNOTATION_PROTOCOL.md
specifies. It only fills in real corpus context + a computed hard-negative stratum HINT (clearly a
hint, not a label) to help annotators stratify their effort.

Output: research/datasets/annotation_sheet_unjudged.csv  (+ prints a summary by stratum).
Run: cd backend && PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/make_annotation_sheet.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data"
OUT = REPO / "research" / "datasets" / "annotation_sheet_unjudged.csv"


def _canon(s: str) -> str:
    return " ".join(str(s).strip().lower().split())


def _skill_overlap(cv_skills, job_skills):
    a = {_canon(s) for s in cv_skills}
    b = {_canon(s) for s in job_skills}
    if not a or not b:
        return 0.0, 0
    inter = a & b
    return len(inter) / len(a | b), len(inter)


def _stratum(overlap, n_shared, title, cv_summary):
    """Heuristic HINT for the annotator's effort stratification (NOT a label):
    - hard_negative: some skill signal but partial (the interesting-to-judge middle)
    - likely_relevant: strong skill overlap (re-judge; may be a missed positive)
    - easy_negative: no shared skills at all."""
    if n_shared == 0:
        return "easy_negative"
    if overlap >= 0.30 or n_shared >= 3:
        return "likely_relevant"
    return "hard_negative"


def main() -> None:
    cvs = {c["id"]: c for c in json.loads((DATA / "cvs.json").read_text())}
    jobs = {j["id"]: j for j in json.loads((DATA / "jobs.json").read_text())}
    labs = json.loads((DATA / "eval_pairs.json").read_text())
    labs = labs.get("labels", labs)
    judged = {(l["query_id"], l["doc_id"]) for l in labs}

    rows = []
    strata = {"hard_negative": 0, "likely_relevant": 0, "easy_negative": 0}
    for cid, cv in cvs.items():
        for jid, job in jobs.items():
            if (cid, jid) in judged:
                continue
            ov, nshared = _skill_overlap(cv.get("skills", []), job.get("required_skills", []))
            stratum = _stratum(ov, nshared, job.get("title", ""), cv.get("summary", ""))
            strata[stratum] += 1
            rows.append({
                "query_id": cid,
                "doc_id": jid,
                "candidate_skills": "; ".join(cv.get("skills", [])),
                "candidate_experience_years": cv.get("experience_years", ""),
                "candidate_summary": (cv.get("summary", "") or "")[:240],
                "job_title": job.get("title", ""),
                "job_required_skills": "; ".join(job.get("required_skills", [])),
                "job_required_experience": job.get("required_experience", ""),
                "job_remote_policy": job.get("remote_policy", ""),
                "shared_skill_count_HINT": nshared,
                "stratum_HINT": stratum,
                # BLANK columns for the humans (0-3 per BENCHMARK_ANNOTATION_PROTOCOL.md rubric):
                "grade_annotator1": "",
                "grade_annotator2": "",
                "adjudicated_grade": "",
                "annotator_rationale": "",
            })

    # Order so annotators can prioritize the informative middle: hard negatives, then likely-relevant,
    # then easy negatives; stable within stratum by (query, doc).
    order = {"hard_negative": 0, "likely_relevant": 1, "easy_negative": 2}
    rows.sort(key=lambda r: (order[r["stratum_HINT"]], r["query_id"], r["doc_id"]))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"wrote {OUT.relative_to(REPO)}  ({len(rows)} currently-unjudged pairs to annotate)")
    print(f"strata (HINT for effort, NOT labels): {strata}")
    print("Grades are BLANK; two independent annotators + an adjudicator fill 0-3 per "
          "BENCHMARK_ANNOTATION_PROTOCOL.md. Combined with the 47 existing labels this yields the full "
          "30x15=450-pair explicitly-judged benchmark (the reviewers' requested explicit negatives).")


if __name__ == "__main__":
    main()
