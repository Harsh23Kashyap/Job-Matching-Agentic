"""Phase 29 / Stage-2 §AB: numerical consistency checker for the ESWA manuscript.

Scans all manuscript .tex (sections + tables) and (1) asserts FORBIDDEN stale/phantom/fabricated
numbers are absent (outside explicit "superseded"/"earlier" correction notes), and (2) confirms the
canonical numbers from research/results/MANUSCRIPT_NUMBERS.json are present. Exit non-zero on any
forbidden hit so it can gate a build.

Run: PYTHONHASHSEED=0 python3 research/experiments/verify_paper_numbers.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SECT = REPO / "docs" / "submission" / "eswa" / "manuscript" / "sections"
TABS = REPO / "docs" / "submission" / "eswa" / "manuscript" / "tables"
MANIFEST = REPO / "research" / "results" / "MANUSCRIPT_NUMBERS.json"

# forbidden: (regex, human description, allowed-context substring or None)
FORBIDDEN = [
    (r"(best|strongest) single[^.]{0,40}0\.969|0\.969[^.]{0,40}(best|strongest) single", "phantom best-single 0.969", None),
    (r"R@5\s*=\s*1\.0(00)?\b", "phantom best-single R@5=1.000", None),
    (r"nine times out of ten", "overclaimed 0.9 => 9/10", None),
    (r"Seven of the ten|7 of 10|seven of ten", "superseded 10-pair counterfactual", None),
    (r"p\s*=\s*0\.048", "salted-seed significance p=0.048", None),
    (r"statistically significant over", "unsupported significance claim", None),
    (r"two independent (reviewers|annotators)", "false two-annotator claim", None),
    (r"12\.3 skills", "fabricated 12.3 skills/resume", None),
    (r"8\.7 (required|req)", "fabricated 8.7 required skills", None),
    (r"4\.2 preferred", "fabricated 4.2 preferred skills", None),
    (r"maximize nDCG@5 on (the |a held-out )?(labeled|held-out)", "B11 weight-tuning claim", None),
    (r"nDCG@5 (maximi[sz]ation|optimi[sz]ation) on", "B11 weight-tuning claim (max/optimization phrasing)", None),
    (r"(fixed|set|tuned|chosen|optimi[sz]ed) by (the )?nDCG", "B11 weights-fitted contradiction", None),
    (r"weights.{0,30}(fixed|set|tuned|chosen|optimi[sz]ed) by (the )?nDCG@?5? optimi[sz]ation", "B11 weights fixed-by-nDCG-optimization (P0.1 leak)", None),
    (r"RRF (ensemble )?.{0,20}0\.935|0\.935.{0,20}RRF", "stale RRF 0.935", None),
]
# canonical numbers that MUST appear somewhere
REQUIRED = ["0.949", "0.878", "0.913", "0.924", "0.019", "2.97", "2.13",
            # Stage-3 graded-skill-channel decomposition (EXP-043/044) + fusion (EXP-035/036 base6)
            "0.917", "0.944", "0.992", "0.942", "0.947", "0.961",
            # Stage-3 calibration campaign (EXP-041): beta ECE + adaptive-ECE exposure of Platt
            "0.009", "0.084"]


def load_text():
    files = list(SECT.glob("*.tex")) + list(TABS.glob("*.tex"))
    return {f.name: f.read_text() for f in files}


def main() -> int:
    texts = load_text()
    blob = "\n".join(texts.values())
    problems, notes = [], []

    for pattern, desc, allowed in FORBIDDEN:
        for fname, txt in texts.items():
            for m in re.finditer(pattern, txt, re.IGNORECASE):
                # context: the line containing the hit
                start = txt.rfind("\n", 0, m.start()) + 1
                end = txt.find("\n", m.end())
                line = txt[start:end if end > 0 else len(txt)]
                if allowed and allowed.lower() in line.lower():
                    notes.append(f"OK (allowed context) [{fname}] {desc}: ...{line.strip()[:90]}")
                    continue
                if re.search(r"superseded|earlier|no longer|we report the held-out|optimistic upper", line, re.IGNORECASE):
                    notes.append(f"OK (correction note) [{fname}] {desc}")
                    continue
                problems.append(f"FORBIDDEN [{fname}] {desc}: ...{line.strip()[:100]}")

    missing = [n for n in REQUIRED if n not in blob]
    for n in missing:
        problems.append(f"MISSING canonical number {n}")

    # cross-check a few manifest numbers appear
    if MANIFEST.exists():
        man = json.loads(MANIFEST.read_text())
        for key in ("ndcg5::Semantic cosine", "ndcg5::RRF ensemble", "composite_ndcg5"):
            if key in man:
                v = f"{man[key]['value']:.3f}"
                if v not in blob:
                    problems.append(f"MANIFEST number {key}={v} not found in manuscript")

    print(f"scanned {len(texts)} tex files")
    for n in notes:
        print("  " + n)
    if problems:
        print("\n=== PROBLEMS ===")
        for p in problems:
            print("  ✗ " + p)
        print(f"\n{len(problems)} problem(s).")
        return 1
    print("\n✓ no forbidden stale numbers; all canonical numbers present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
