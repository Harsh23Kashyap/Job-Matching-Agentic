"""Stage-2 §30/§AA: regenerate the reliability diagram (fig4) from HELD-OUT calibration data.

The old fig4 was the in-sample curve (audit). This plots the held-out 5-fold reliability curves
for the raw composite, Platt, and isotonic maps directly from calibration_methods.json (EXP-026),
so the figure matches the reported held-out numbers. Overwrites the committed PNG.

Run: cd backend && PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/make_reliability_fig.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "research" / "results" / "calibration_methods.json"
OUT = REPO / "docs" / "submission" / "eswa" / "manuscript" / "figures" / "fig4_reliability_diagram.png"


def curve_xy(method_curve):
    xs, ys = [], []
    for b in method_curve:
        if b["mean_pred"] is None:
            continue
        xs.append(b["mean_pred"]); ys.append(b["frac_pos"])
    return xs, ys


def main() -> None:
    d = json.loads(SRC.read_text())
    m = d["methods"]
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    ax.plot([0, 1], [0, 1], "k--", lw=1, label="Perfect calibration")
    styles = {"raw": ("#e69f00", "o", f"Raw composite (ECE {m['raw']['ece']:.3f})"),
              "platt": ("#009e73", "s", f"Platt (ECE {m['platt']['ece']:.3f}, held-out)"),
              "isotonic": ("#56b4e9", "^", f"Isotonic (ECE {m['isotonic']['ece']:.3f}, held-out)"),
              "beta": ("#cc79a7", "D", f"Beta (ECE {m['beta']['ece']:.3f}, held-out; recommended)")}
    for meth, (c, mk, lbl) in styles.items():
        xs, ys = curve_xy(m[meth]["reliability_curve"])
        ax.plot(xs, ys, marker=mk, color=c, lw=1.6, ms=6, label=lbl)
    ax.set_xlabel("Predicted probability (confidence)")
    ax.set_ylabel("Empirical relevance frequency")
    ax.set_title("Reliability diagram (held-out 5-fold)")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.legend(loc="upper left", fontsize=8, frameon=True)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
