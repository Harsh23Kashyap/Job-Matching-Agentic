"""Produce anonymized copies of the author-facing documentation for the double-blind reviewer bundle.

The manuscript body and the released test fixtures are already anonymized; the ESWA title page and
cover letter are the (correctly) non-anonymous parts of the submission and are NOT touched. This script
covers the remaining gap flagged in review: the project README and design docs still carry author
identity + the real repository URL, which must be scrubbed in the copy that ships alongside the
ANONYMIZED manuscript. It writes scrubbed copies under build/anon/ (it never mutates the working tree,
so real attribution is preserved for the public release on acceptance) and then verifies that no
author identifier survives in the copy.

Run: python3 scripts/anonymize_reviewer_bundle.py
Exit code 0 = anonymized copies written and verified clean; non-zero = a residual identifier remains.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "build" / "anon"

# Files that ship in the reviewer artifact bundle and must be anonymized (paths relative to REPO).
FILES = [
    "README.md",
    "docs/design/HLD-multi-agent-system.md",
    "docs/design/SDD-multi-agent-system.md",
    "docs/design/V1-V2-SCOPE.md",
]

# Ordered replacements (specific -> general). Case-insensitive where a lowercase variant exists.
SUBS = [
    (r"https?://github\.com/Harsh23Kashyap/[^\s)\]]*", "https://anonymous.4open.science/r/JobMatch"),
    (r"github\.com/Harsh23Kashyap/[^\s)\]]*", "anonymous.4open.science/r/JobMatch"),
    (r"linkedin\.com/in/[A-Za-z0-9\-]+", "linkedin.com/in/anonymous"),
    (r"Harsh\s+Kashyap", "Anonymous Author"),
    (r"Taranumpreet\s+Kaur\s+Wasu", "Anonymous Author"),
    (r"Parteek\s+Kumar", "Anonymous Supervisor"),
    (r"Thapar\s+Institute[^.\n,)]*", "Anonymous Institution"),
    (r"Washington\s+State\s+University", "Anonymous University"),
    (r"Kashyap", "Anonymous"),
    (r"Taranum\w*", "Anonymous"),
]

# Anything matching these (case-insensitive) in the OUTPUT is a failure.
LEAK_PATTERNS = [r"kashyap", r"taranum", r"thapar", r"harsh23kashyap", r"linkedin\.com/in/harsh", r"parteek"]


def anonymize_text(text: str) -> str:
    for pat, repl in SUBS:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE if pat[0].islower() or "\\s" in pat else 0)
    return text


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    problems = []
    written = []
    for rel in FILES:
        src = REPO / rel
        if not src.exists():
            print(f"skip (missing): {rel}")
            continue
        anon = anonymize_text(src.read_text(encoding="utf-8"))
        dst = OUT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(anon, encoding="utf-8")
        written.append(rel)
        for lp in LEAK_PATTERNS:
            if re.search(lp, anon, flags=re.IGNORECASE):
                problems.append(f"{rel}: residual identifier matching /{lp}/")
    print(f"anonymized {len(written)} file(s) into {OUT.relative_to(REPO)}: {', '.join(written)}")
    if problems:
        print("\n=== ANONYMIZATION INCOMPLETE ===")
        for p in problems:
            print("  x " + p)
        return 1
    print("verified: no author identifier remains in the anonymized copies.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
