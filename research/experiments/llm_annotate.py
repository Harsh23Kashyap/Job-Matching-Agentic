"""LLM-ASSISTED annotation of the 403 currently-unjudged (resume, job) pairs, via Kiro (two model
families for inter-model agreement). Produces PROVISIONAL explicit-negative labels so the powered
re-test can be run now; these are DISCLOSED as LLM-assisted (extending the paper's existing
LLM-assisted second pass, kappa=0.69) and are NOT human ground truth. The human (author) does the
authoritative pass before submission — this pre-fills the sheet to make that review fast, and never
fabricates: grades come from the models, disagreements are flagged, failures are logged (no silent gaps).

Two LLM annotators: gpt-5.6-sol and deepseek-3.2 (distinct families) via consult-kiro.sh.
Per candidate: one prompt lists the profile + its unjudged jobs; the model returns JSON {job_id: grade 0-3}.
Adjudication: agree -> that grade; |diff|=1 -> round(mean); |diff|>=2 -> flag + conservative (min).
Reports quadratic-weighted kappa + grade distribution + coverage. Writes an LLM-labeled sheet copy and,
if coverage is sufficient, an eval_pairs_llm_expanded.json for powered_reeval.py.

Run: cd backend && PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/llm_annotate.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data"
OUT_SHEET = REPO / "research" / "datasets" / "annotation_sheet_llm_prefilled.csv"
OUT_EVAL = DATA / "eval_pairs_llm_expanded.json"
OUT_REPORT = REPO / "research" / "results" / "llm_annotation.json"
SK = Path(os.path.expanduser("~/.kiro/skills/consult-kiro/scripts/consult-kiro.sh"))
if not SK.exists():
    SK = Path(os.path.expanduser("~/.claude/skills/consult-kiro/scripts/consult-kiro.sh"))
MODELS = ["gpt-5.6-sol", "deepseek-3.2"]
MAX_WORKERS = 3
CALL_TIMEOUT = 240

RUBRIC = ("Grade each (resume, job) pair 0-3 for advancing to a first interview: "
          "3=strong (meets required skills+seniority), 2=plausible (most requirements, minor gaps), "
          "1=weak (missing a key required skill OR wrong seniority band), 0=unqualified (wrong domain / "
          "missing most requirements). Judge on content only; ignore name/gender/age/location. Required "
          "skills weigh more than nice-to-haves.")


def _prompt(cv: dict, jobs: list[dict]) -> str:
    lines = [RUBRIC, "",
             f"CANDIDATE {cv['id']}: skills=[{', '.join(cv.get('skills', []))}]; "
             f"experience_years={cv.get('experience_years')}; summary={(cv.get('summary') or '')[:300]}", "",
             "JOBS to grade for this candidate:"]
    for j in jobs:
        lines.append(f"- {j['id']}: title={j.get('title')}; required_skills=[{', '.join(j.get('required_skills', []))}]; "
                     f"required_experience={j.get('required_experience')}; remote_policy={j.get('remote_policy')}")
    lines += ["", "Return ONLY a JSON object mapping each job_id to an integer grade 0-3, e.g. "
              '{"job_03": 0, "job_07": 2}. No prose, no code fences.']
    return "\n".join(lines)


def _extract_grades(text: str, jids: list[str]) -> dict:
    m = re.search(r"\{[^{}]*\}", text, re.DOTALL)
    if not m:
        return {}
    try:
        raw = json.loads(m.group(0))
    except Exception:
        return {}
    out = {}
    for jid in jids:
        v = raw.get(jid)
        if isinstance(v, (int, float)) and 0 <= int(v) <= 3:
            out[jid] = int(v)
    return out


def _grade_one(model: str, cv: dict, jobs: list[dict]) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write(_prompt(cv, jobs)); pth = f.name
    try:
        r = subprocess.run(["bash", str(SK), "--model", model, "--effort", "medium", "--file", pth],
                           capture_output=True, text=True, timeout=CALL_TIMEOUT)
        return _extract_grades(r.stdout, [j["id"] for j in jobs])
    except Exception:
        return {}
    finally:
        os.unlink(pth)


def _kappa_quadratic(pairs: list[tuple[int, int]]) -> float:
    if not pairs:
        return float("nan")
    import numpy as np
    a = np.array([p[0] for p in pairs]); b = np.array([p[1] for p in pairs])
    cats = [0, 1, 2, 3]; n = len(pairs)
    O = np.zeros((4, 4))
    for x, y in pairs:
        O[x, y] += 1
    O /= n
    ra = np.array([np.mean(a == c) for c in cats]); rb = np.array([np.mean(b == c) for c in cats])
    E = np.outer(ra, rb)
    W = np.array([[((i - j) ** 2) / 9.0 for j in cats] for i in cats])
    num = (W * O).sum(); den = (W * E).sum()
    return float(1 - num / den) if den > 0 else float("nan")


def main() -> None:
    cvs = {c["id"]: c for c in json.loads((DATA / "cvs.json").read_text())}
    jobs = {j["id"]: j for j in json.loads((DATA / "jobs.json").read_text())}
    worklist = json.loads(Path("/tmp/annot_worklist.json").read_text())["cvs_with_unjudged"]
    print(f"annotating {sum(len(v) for v in worklist.values())} pairs across {len(worklist)} candidates "
          f"with {MODELS} (max_workers={MAX_WORKERS}) ...")

    import threading
    CACHE = REPO / "research" / "results" / ".annot_cache.json"
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    lock = threading.Lock()
    ck = lambda m, c: f"{m}|{c}"
    tasks = [(model, cid, jids) for cid, jids in worklist.items() for model in MODELS]
    todo = [t for t in tasks if ck(t[0], t[1]) not in cache]
    print(f"resumable cache: {len(cache)} done, {len(todo)} to do (of {len(tasks)})")

    def run(task):
        model, cid, jids = task
        g = _grade_one(model, cvs[cid], [jobs[j] for j in jids])
        with lock:
            cache[ck(model, cid)] = g
            CACHE.write_text(json.dumps(cache))  # checkpoint after every call -> survives timeout/kill
        return ck(model, cid), len(g), len(jids)

    if todo:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
            for k, n, tot in ex.map(run, todo):
                print(f"  {k}: {n}/{tot} graded")
    results: dict[tuple[str, str], dict] = {tuple(k.split("|", 1)): g for k, g in cache.items()}

    # assemble per-pair grades from the two models + adjudicate
    rows, kappa_pairs, flagged = [], [], 0
    for cid, jids in worklist.items():
        gA = results.get((MODELS[0], cid), {}); gB = results.get((MODELS[1], cid), {})
        for jid in jids:
            a, b = gA.get(jid), gB.get(jid)
            adj, flag = None, ""
            if a is not None and b is not None:
                kappa_pairs.append((a, b))
                if a == b:
                    adj = a
                elif abs(a - b) == 1:
                    adj = round((a + b) / 2)
                else:
                    adj = min(a, b); flag = "disagree>=2"; flagged += 1
            elif a is not None:
                adj = a
            elif b is not None:
                adj = b
            rows.append({"query_id": cid, "doc_id": jid, "grade_gpt": a, "grade_deepseek": b,
                         "adjudicated_grade": adj, "flag": flag})

    covered = [r for r in rows if r["adjudicated_grade"] is not None]
    kappa = _kappa_quadratic(kappa_pairs)
    dist = {g: sum(1 for r in covered if r["adjudicated_grade"] == g) for g in (0, 1, 2, 3)}

    import csv
    with OUT_SHEET.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

    # build an LLM-expanded eval file (existing human 47 + LLM-adjudicated negatives/positives), DISCLOSED
    base = json.loads((DATA / "eval_pairs.json").read_text())
    labels = list(base.get("labels", []))
    seen = {(l["query_id"], l["doc_id"]) for l in labels}
    added = 0
    for r in covered:
        key = (r["query_id"], r["doc_id"])
        if key in seen:
            continue
        labels.append({"query_id": r["query_id"], "doc_id": r["doc_id"], "relevance": int(r["adjudicated_grade"]),
                       "source": "llm_assisted"})
        added += 1
    base_out = dict(base); base_out["labels"] = labels
    base_out["notes"] = (base.get("notes", "") + " | LLM-ASSISTED expansion: 403 previously-unjudged pairs "
                         "graded by gpt-5.6-sol + deepseek-3.2 (adjudicated); PROVISIONAL, not human ground "
                         "truth; author review pending before submission.")
    OUT_EVAL.write_text(json.dumps(base_out, indent=1))

    report = {"experiment": "LLM-assisted annotation of unjudged pairs (provisional, disclosed)",
              "models": MODELS, "n_target_pairs": len(rows), "n_covered": len(covered),
              "coverage_rate": round(len(covered) / len(rows), 3),
              "inter_model_quadratic_kappa": round(kappa, 3) if kappa == kappa else None,
              "n_flagged_disagree_ge2": flagged, "adjudicated_grade_distribution": dist,
              "explicit_negatives_added": dist.get(0, 0),
              "outputs": {"sheet": str(OUT_SHEET.relative_to(REPO)), "eval": str(OUT_EVAL.relative_to(REPO))},
              "caveat": "LLM-assisted PROVISIONAL labels for a powered dry-run; NOT human ground truth. "
                        "Run powered_reeval.py with EVAL_PAIRS=data/eval_pairs_llm_expanded.json."}
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
