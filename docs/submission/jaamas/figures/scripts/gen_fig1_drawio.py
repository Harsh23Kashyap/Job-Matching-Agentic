#!/usr/bin/env python3
"""Generate Fig 1 HLD draw.io source (JobMatch multi-agent overview)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from drawio_emit import (  # noqa: E402
    PALETTE,
    bold_lines,
    box_style,
    cell_edge,
    cell_edge_points,
    cell_vertex,
    write_mxfile,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source" / "Fig1.drawio"
PAGE_W, PAGE_H = 1000, 520

COL_W, BOX_H = 260, 68
X_L, X_C, X_R = 50, 370, 690
Y1, Y2, Y3 = 48, 148, 248


def gen_fig1() -> None:
    c = PALETTE
    cells = [
        # Candidate side
        cell_vertex(
            "js",
            bold_lines("Job seeker", "uses candidate portal"),
            X_L,
            Y1,
            COL_W,
            BOX_H,
            box_style(*c["actor_c"]),
        ),
        cell_vertex(
            "cp",
            bold_lines("Candidate portal", "onboarding · profile · matches"),
            X_L,
            Y2,
            COL_W,
            BOX_H,
            box_style(*c["portal"]),
        ),
        cell_vertex(
            "ca",
            bold_lines("Candidate agent", "owns candidate state"),
            X_L,
            Y3,
            COL_W,
            BOX_H,
            box_style(*c["agent_c"]),
        ),
        # Platform core
        cell_vertex(
            "ad",
            bold_lines("Admin / evaluation", "benchmarks · fairness · reset"),
            X_C,
            Y1,
            COL_W,
            BOX_H,
            box_style(*c["admin"]),
        ),
        cell_vertex(
            "ma",
            bold_lines("Matchmaking agent", "read-only broker"),
            X_C,
            Y2,
            COL_W,
            BOX_H + 12,
            box_style(*c["broker"]),
        ),
        # Employer side
        cell_vertex(
            "em",
            bold_lines("Employer / recruiter", "uses employer portal"),
            X_R,
            Y1,
            COL_W,
            BOX_H,
            box_style(*c["actor_e"]),
        ),
        cell_vertex(
            "ep",
            bold_lines("Employer portal", "postings · shortlist · applicants"),
            X_R,
            Y2,
            COL_W,
            BOX_H,
            box_style(*c["portal"]),
        ),
        cell_vertex(
            "ea",
            bold_lines("Employer agent", "owns job state"),
            X_R,
            Y3,
            COL_W,
            BOX_H,
            box_style(*c["agent_e"]),
        ),
        # Vertical ownership chains
        cell_edge("e_js_cp", "js", "cp"),
        cell_edge("e_cp_ca", "cp", "ca"),
        cell_edge("e_em_ep", "em", "ep"),
        cell_edge("e_ep_ea", "ep", "ea"),
        # Admin → matcher (evaluation only)
        cell_edge("e_ad_ma", "ad", "ma", "evaluation", dashed=True),
        # Agent ↔ matcher
        cell_edge(
            "e_ca_ma",
            "ca",
            "ma",
            "snapshots and events",
            exit_x=1,
            exit_y=0.5,
            entry_x=0,
            entry_y=0.5,
        ),
        cell_edge(
            "e_ea_ma",
            "ea",
            "ma",
            "snapshots and events",
            exit_x=0,
            exit_y=0.5,
            entry_x=1,
            entry_y=0.5,
        ),
        # Ranked results → portals
        cell_edge_points(
            "e_ma_cp",
            "ma",
            "cp",
            [(X_C + COL_W / 2, Y1 + BOX_H / 2 + 8)],
            "ranked matches",
            exit_x=0.25,
            exit_y=0,
            entry_x=0.75,
            entry_y=1,
        ),
        cell_edge_points(
            "e_ma_ep",
            "ma",
            "ep",
            [(X_C + COL_W / 2, Y1 + BOX_H / 2 + 8)],
            "ranked candidates",
            exit_x=0.75,
            exit_y=0,
            entry_x=0.25,
            entry_y=1,
        ),
    ]
    write_mxfile(OUT, "Fig1", PAGE_W, PAGE_H, cells)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    gen_fig1()
