"""EXP-018: LLM-assisted relevance label expansion via headless `claude -p` (RD-005).

Expands toward the full 30x15=450 grid using an LLM annotator (local `claude -p`, NO external API).
One call per resume rates all 15 jobs on the 0-2 rubric. Output is EXPLICITLY marked LLM-assisted,
NOT human judgments; the 47 human/author labels remain the anchor. Reports Cohen's weighted kappa +
raw/within-1 agreement of the LLM vs the human anchor on the 47 labeled pairs.

Run (slow, ~30 claude calls): cd backend && PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/llm_label_expansion.py
"""
from __future__ import annotations
import json
import re
import subprocess
from pathlib import Path

from sklearn.metrics import cohen_kappa_score, confusion_matrix

from config import Settings
from core.document_text import job_document_text, resume_document_text
from benchmarks.eval_data import load_eval_labels

REPO = Path(__file__).resolve().parents[2]
RUBRIC = (
    "You are a careful recruitment relevance annotator. Rate how relevant each JOB is for the "
    "CANDIDATE on this scale: 2 = strong match (candidate meets the core required skills and "
    "experience level); 1 = partial match (some required skills/experience overlap, with clear "
    "gaps); 0 = not relevant (little or no overlap)."
)


def call_claude(prompt: str, timeout: int = 180) -> str:
    # `claude` binary (subprocess bypasses the shell wrapper). Headless print mode, no external API.
    res = subprocess.run(["claude", "-p", prompt, "--output-format", "text"],
                         capture_output=True, text=True, timeout=timeout)
    return res.stdout.strip()


def parse_json(text: str):
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def main() -> None:
    settings = Settings()
    cvs = json.load(open(settings.data_dir / "cvs.json"))
    jobs = json.load(open(settings.data_dir / "jobs.json"))
    human = load_eval_labels(settings.data_dir / "eval_pairs.json")  # {qid:{jid:grade}}
    job_ids = [j["id"] for j in jobs]
    job_block = "\n".join(f"[{j['id']}] {job_document_text(j)}" for j in jobs)

    llm_labels = []          # eval_pairs-format
    grid = {}                # qid -> {jid: grade}
    failures = []
    for cv in cvs:
        qid = cv["id"]
        prompt = (
            f"{RUBRIC}\n\nCANDIDATE:\n{resume_document_text(cv)}\n\n"
            f"JOBS (rate every one):\n{job_block}\n\n"
            f"Respond with ONLY compact JSON mapping each job id to an integer grade 0, 1, or 2. "
            f'Example: {{"job_01":2,"job_02":0}}. Rate all {len(jobs)} jobs. No prose.'
        )
        obj = None
        for _ in range(2):  # one retry
            try:
                obj = parse_json(call_claude(prompt))
            except Exception as e:
                failures.append(f"{qid}: {e!r}")
                obj = None
            if isinstance(obj, dict):
                break
        grid[qid] = {}
        for jid in job_ids:
            g = 0
            if isinstance(obj, dict) and jid in obj:
                try:
                    g = max(0, min(2, int(obj[jid])))
                except Exception:
                    g = 0
            grid[qid][jid] = g
            llm_labels.append({"query_id": qid, "doc_id": jid, "relevance": g})
        print(f"  labeled {qid}: {sum(grid[qid].values())} total grade-points across {len(jobs)} jobs", flush=True)

    # agreement vs human anchor (only the 47 human-labeled pairs)
    h, l = [], []
    for qid, rels in human.items():
        for jid, hg in rels.items():
            h.append(int(hg)); l.append(int(grid.get(qid, {}).get(jid, 0)))
    kappa = float(cohen_kappa_score(h, l, weights="quadratic")) if len(set(h)) > 1 and len(set(l)) > 1 else None
    raw = float(sum(1 for a, b in zip(h, l) if a == b) / len(h)) if h else None
    within1 = float(sum(1 for a, b in zip(h, l) if abs(a - b) <= 1) / len(h)) if h else None
    labels_sorted = sorted(set(h) | set(l))
    cm = confusion_matrix(h, l, labels=labels_sorted).tolist() if h else []

    # save LLM-labeled set (clearly marked non-human)
    (settings.data_dir / "eval_pairs_llm.json").write_text(json.dumps({
        "version": "1.0-LLM",
        "task": "resume_to_jobs",
        "relevance_scale": "0-2",
        "provenance": "LLM-ASSISTED via local `claude -p` (NOT human judgments). Human 47-pair set (eval_pairs.json) remains the anchor. RD-005.",
        "labels": llm_labels,
    }, indent=2))

    report = {
        "experiment": "EXP-018 LLM-assisted label expansion (claude -p, RD-005)",
        "provenance": "LLM-ASSISTED, NOT human. 47 human labels remain the anchor.",
        "n_llm_labels": len(llm_labels), "n_resumes": len(cvs), "n_jobs": len(jobs),
        "grade_distribution_llm": {str(g): sum(1 for x in llm_labels if x["relevance"] == g) for g in (0, 1, 2)},
        "agreement_vs_human_anchor": {
            "n_anchor_pairs": len(h),
            "cohen_kappa_quadratic": round(kappa, 4) if kappa is not None else None,
            "raw_exact_agreement": round(raw, 4) if raw is not None else None,
            "within_1_agreement": round(within1, 4) if within1 is not None else None,
            "confusion_labels": labels_sorted, "confusion_matrix_human_rows_llm_cols": cm,
            "note": "Human anchor has only grades 1,2 (no explicit 0s); kappa/agreement computed on those 47 pairs.",
        },
        "n_call_failures": len(failures), "failures": failures[:10],
        "interpretation": (
            "This is an LLM-labeled DENSITY set for stress/robustness/scale checks and a second-annotator "
            "signal, NOT a human benchmark. Report kappa honestly; the primary ranking benchmark stays the "
            "47 human/author labels. Do not present these as human relevance judgments (RD-005/§15)."
        ),
    }
    outdir = REPO / "research" / "results"; outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "llm_label_expansion.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report[k] for k in ("n_llm_labels", "grade_distribution_llm", "agreement_vs_human_anchor", "n_call_failures")}, indent=2))


if __name__ == "__main__":
    main()
