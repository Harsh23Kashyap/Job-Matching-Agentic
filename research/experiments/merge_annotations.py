"""Merge a completed annotation sheet (adjudicated grades filled) back into the eval-pairs format,
producing the EXPANDED, explicitly-judged benchmark that the existing evaluation harness consumes.

Pipeline: make_annotation_sheet.py -> [two annotators + adjudicator fill 0-3] -> merge_annotations.py
-> data/eval_pairs_expanded.json -> re-run the existing harness (extended_evaluation / comparison /
graded_skill_channel) pointed at the expanded file for a POWERED, explicitly-negative-judged re-test.

This is deterministic glue; it fabricates nothing. It reads the human-filled `adjudicated_grade`
column (blank rows are skipped), unions them with the existing 47 labels, and writes the same schema.

Usage:
  python3 research/experiments/merge_annotations.py            # merge the real sheet (skips blank rows)
  python3 research/experiments/merge_annotations.py --selftest # validate merge logic (no files written)
"""
from __future__ import annotations

import csv
import json
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EVAL = REPO / "data" / "eval_pairs.json"
SHEET = REPO / "research" / "datasets" / "annotation_sheet_unjudged.csv"
OUT = REPO / "data" / "eval_pairs_expanded.json"


def merge(eval_path: Path, sheet_path: Path) -> dict:
    base = json.loads(eval_path.read_text())
    labels = list(base.get("labels", []))
    seen = {(l["query_id"], l["doc_id"]) for l in labels}
    added = 0
    with sheet_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            g = (row.get("adjudicated_grade") or "").strip()
            if g == "":
                continue
            grade = int(g)
            if grade < 0 or grade > 3:
                raise ValueError(f"grade out of range 0-3: {grade} for {row['query_id']}/{row['doc_id']}")
            key = (row["query_id"], row["doc_id"])
            if key in seen:
                continue  # never overwrite an existing judged label
            labels.append({"query_id": row["query_id"], "doc_id": row["doc_id"], "relevance": grade})
            seen.add(key)
            added += 1
    out = dict(base)
    out["labels"] = labels
    out["notes"] = (base.get("notes", "") + " | EXPANDED with explicitly-judged pairs from "
                    "annotation_sheet_unjudged.csv (merge_annotations.py); grades 0-3 human-adjudicated.")
    return out, added


def _selftest() -> int:
    """Validate merge logic with a tiny synthetic sheet (2 filled rows incl. an explicit 0) — no real files written."""
    base = {"version": "t", "task": "t", "relevance_scale": "0-3", "notes": "n",
            "labels": [{"query_id": "cv_01", "doc_id": "job_01", "relevance": 2}]}
    rows = [
        {"query_id": "cv_01", "doc_id": "job_02", "adjudicated_grade": "0"},   # explicit negative
        {"query_id": "cv_02", "doc_id": "job_03", "adjudicated_grade": "3"},   # strong
        {"query_id": "cv_09", "doc_id": "job_09", "adjudicated_grade": ""},    # blank -> skipped
        {"query_id": "cv_01", "doc_id": "job_01", "adjudicated_grade": "1"},   # dup of existing -> not overwritten
    ]
    with tempfile.TemporaryDirectory() as d:
        ep = Path(d) / "e.json"; sp = Path(d) / "s.csv"
        ep.write_text(json.dumps(base))
        with sp.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["query_id", "doc_id", "adjudicated_grade"]); w.writeheader(); w.writerows(rows)
        out, added = merge(ep, sp)
    labs = {(l["query_id"], l["doc_id"]): l["relevance"] for l in out["labels"]}
    assert added == 2, f"expected 2 added, got {added}"
    assert labs[("cv_01", "job_02")] == 0, "explicit negative not merged"
    assert labs[("cv_02", "job_03")] == 3, "grade-3 not merged"
    assert labs[("cv_01", "job_01")] == 2, "existing label was overwritten (must not happen)"
    assert ("cv_09", "job_09") not in labs, "blank row was merged (must be skipped)"
    grades = sorted(set(labs.values()))
    assert 0 in grades, "no explicit negative in merged set"
    print("SELFTEST PASS: 2 merged (incl. explicit 0), blank skipped, existing label preserved, "
          f"grade range now {grades}")
    return 0


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()
    if not SHEET.exists():
        print(f"annotation sheet not found: {SHEET} (run make_annotation_sheet.py first)"); return 1
    out, added = merge(EVAL, SHEET)
    dist = {g: sum(1 for l in out["labels"] if l["relevance"] == g) for g in (0, 1, 2, 3)}
    if added == 0:
        print(f"No adjudicated grades filled in {SHEET.name} yet (0 rows merged). "
              f"Fill the `adjudicated_grade` column (0-3), then re-run. Existing labels: {len(out['labels'])}.")
        return 0
    OUT.write_text(json.dumps(out, indent=1))
    print(f"wrote {OUT.relative_to(REPO)}: {len(out['labels'])} labels ({added} newly added). Grade distribution: {dist}")
    print("Next: point the harness at this file, e.g. re-run comparison_table / graded_skill_channel "
          "with eval_pairs_expanded.json for the powered, explicitly-negative-judged re-test.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
