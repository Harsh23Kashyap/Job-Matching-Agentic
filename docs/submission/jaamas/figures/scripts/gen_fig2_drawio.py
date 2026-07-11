#!/usr/bin/env python3
"""Generate Fig 2 (Candidate workflow) drawio source.

Redesign v2: proper swimlane pool with parallel lanes, vertical lifelines,
orthogonal edges between lifelines, and activity notes placed inside the
candidate agent lane only.

Layout:
- Page 1700x600
- One horizontal pool header at top with 6 lane cells
- Lifelines drop from each lane header to the bottom
- Messages route between lifelines at fixed Y rows
- Activity notes sit inside the candidate agent lane
- Self-messages use a small U-shape to the right of the lifeline
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source" / "Fig2.drawio"

PAGE_W, PAGE_H = 1700, 600

ACTORS = ["Candidate", "Parser", "Candidate\nAgent", "Matchmaking\nAgent", "Matching\nCore", "Portal"]
ACTOR_FILL = ["#eef2ff", "#fff7ed", "#ecfdf5", "#eff6ff", "#faf5ff", "#f1f5f9"]
ACTOR_STROKE = ["#4338ca", "#b45309", "#047857", "#2563eb", "#7c3aed", "#475569"]

LANE_W = 240
LANE_GAP = 26
LANE_Y = 36
LANE_H = 56

NUM_LANES = len(ACTORS)
TOTAL_W = NUM_LANES * LANE_W + (NUM_LANES - 1) * LANE_GAP
LANE_X0 = (PAGE_W - TOTAL_W) / 2

LIFELINE_TOP = LANE_Y + LANE_H + 10
LIFELINE_BOTTOM = PAGE_H - 24


def x(i: int) -> float:
    return LANE_X0 + i * (LANE_W + LANE_GAP) + LANE_W / 2


def x_left(i: int) -> float:
    return LANE_X0 + i * (LANE_W + LANE_GAP)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def lane_box_xml(cid: str, x: float, y: float, w: float, h: float, value: str, fill: str, stroke: str,
                 font: int = 13) -> str:
    body = esc(value).replace("\n", "&#10;")
    style = (
        f"rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
        f"fontSize={font};fontFamily=Helvetica;fillColor={fill};strokeColor={stroke};strokeWidth=1.5;"
    )
    return (
        f'        <mxCell id="{cid}" value="{body}" style="{style}" vertex="1" parent="1">\n'
        f'          <mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/>\n'
        f"        </mxCell>"
    )


def lane_bg_xml(cid: str, x: float, y: float, w: float, h: float, fill: str, stroke: str = "#cbd5e1") -> str:
    """Light lane background panel."""
    style = (
        f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
        f"strokeWidth=1;dashed=0;opacity=70;"
    )
    return (
        f'        <mxCell id="{cid}" value="" style="{style}" vertex="1" parent="1">\n'
        f'          <mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/>\n'
        f"        </mxCell>"
    )


def lifeline_xml(cid: str, lane: int) -> str:
    style = (
        "endArrow=none;html=1;rounded=0;strokeColor=#94a3b8;strokeWidth=1.5;dashed=1;"
        "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryDy=0;"
    )
    return (
        f'        <mxCell id="{cid}" style="{style}" edge="1" parent="1" source="actor_{lane}" target="actor_{lane}">\n'
        f'          <mxGeometry relative="1" as="geometry">\n'
        f'            <mxPoint x="0" y="{LIFELINE_TOP}" as="sourcePoint"/>\n'
        f'            <mxPoint x="0" y="{LIFELINE_BOTTOM}" as="targetPoint"/>\n'
        f"          </mxGeometry>\n"
        f"        </mxCell>"
    )


def msg_xml(eid: str, src: int, dst: int, y: float, label: str) -> str:
    sx, dx = x(src), x(dst)
    body = esc(label)
    style = (
        "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=1.8;strokeColor=#1e293b;"
        "fontSize=12;fontColor=#0f172a;endArrow=blockThin;endFill=1;"
        "labelBackgroundColor=#ffffff;align=center;verticalAlign=middle;"
    )
    if src == dst:
        return (
            f'        <mxCell id="{eid}" value="{body}" style="{style}" edge="1" parent="1" source="life_{src}" target="life_{dst}">\n'
            f'          <mxGeometry relative="1" as="geometry">\n'
            f'            <mxPoint x="{sx + 60:.1f}" y="{y - 18:.1f}" as="sourcePoint"/>\n'
            f'            <mxPoint x="{sx + 60:.1f}" y="{y + 8:.1f}" as="targetPoint"/>\n'
            f"          </mxGeometry>\n"
            f"        </mxCell>"
        )
    # Connect with explicit exit/entry so drawio draws a horizontal arrow
    # between the two lifelines at the given y. No Array needed for this style.
    if src < dst:
        side = "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"
    else:
        side = "exitX=0;exitY=0.5;entryX=1;entryY=0.5;"
    style += side
    return (
        f'        <mxCell id="{eid}" value="{body}" style="{style}" edge="1" parent="1" source="life_{src}" target="life_{dst}">\n'
        f'          <mxGeometry relative="1" as="geometry"/>\n'
        f"        </mxCell>"
    )


def note_xml(cid: str, x: float, y: float, w: float, h: float, value: str) -> str:
    body = esc(value)
    style = (
        "rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
        "fontSize=11;fontFamily=Helvetica;fillColor=#ffffff;strokeColor=#94a3b8;"
        "strokeWidth=1;dashed=1;"
    )
    return (
        f'        <mxCell id="{cid}" value="{body}" style="{style}" vertex="1" parent="1">\n'
        f'          <mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/>\n'
        f"        </mxCell>"
    )


def gen_fig2() -> None:
    cells: list[str] = []
    cells.append(lane_box_xml("title", 0, 0, PAGE_W, 30,
                              "Fig. 2  Candidate workflow (profile to matches)",
                              "#f1f5f9", "#334155", font=14))

    # Lane backgrounds (alternating subtle tints)
    for i in range(NUM_LANES):
        bg_fill = "#f8fafc" if i % 2 == 0 else "#ffffff"
        cells.append(lane_bg_xml(
            f"bg_{i}", x_left(i), LANE_Y - 6, LANE_W, PAGE_H - LANE_Y - 30, bg_fill
        ))

    # Lane headers
    for i, name in enumerate(ACTORS):
        cells.append(lane_box_xml(
            f"actor_{i}", x_left(i), LANE_Y, LANE_W, LANE_H,
            name, ACTOR_FILL[i], ACTOR_STROKE[i], font=13
        ))

    # Lifelines
    for i in range(NUM_LANES):
        cells.append(lifeline_xml(f"life_{i}", i))

    # Row 1: ingest (Candidate -> Parser -> Candidate Agent) at y=140
    r1 = 140
    cells.append(msg_xml("m1a", 0, 1, r1, "Upload resume or paste text"))
    cells.append(msg_xml("m1b", 1, 2, r1 + 30, "Clean text and extract fields"))

    # Row 2: candidate agent internal + confirm (y=220..320)
    r2 = 240
    cells.append(msg_xml("m2a", 2, 0, r2, "Profile draft pre-filled in form"))
    cells.append(msg_xml("m2_self", 2, 2, r2 + 30, "Normalize, quality-check, embed"))
    cells.append(msg_xml("m2b", 0, 2, r2 + 60, "User confirms profile"))
    cells.append(msg_xml("m2c", 2, 2, r2 + 90, "Store snapshot + upsert vector"))
    cells.append(msg_xml("m2d", 2, 3, r2 + 120, "Emit profile-updated event"))

    # Row 3: matchmaking (y=400)
    r3 = 420
    cells.append(msg_xml("m3a", 0, 3, r3, "Click Find matches"))
    cells.append(msg_xml("m3_self", 3, 3, r3 + 30, "Load candidate + job snapshots"))
    cells.append(msg_xml("m3b", 3, 4, r3 + 60, "Score and rank pairs (read-only)"))

    # Row 4: results back (y=520)
    r4 = 540
    cells.append(msg_xml("m4a", 4, 3, r4, "Return ranked list with explanations"))
    cells.append(msg_xml("m4b", 3, 5, r4 + 24, "Render results in portal"))
    cells.append(msg_xml("m4c", 0, 5, r4 + 48, "Save, apply, or dismiss"))

    body = "\n".join(cells)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<mxfile host="app.diagrams.net" modified="2026-07-12T01:30:00.000Z" '
        'agent="gen_fig2_drawio.py" version="22.1.0">\n'
        '  <diagram name="Figure 2" id="PgyecS3JJFfJTJn-FHwx-rev4">\n'
        f'    <mxGraphModel dx="{PAGE_W}" dy="{PAGE_H}" grid="1" gridSize="10" guides="1" tooltips="1" '
        'connect="1" arrows="1" fold="1" page="1" pageScale="1" '
        f'pageWidth="{PAGE_W}" pageHeight="{PAGE_H}" math="0" shadow="0">\n'
        '      <root>\n'
        '        <mxCell id="0"/>\n'
        '        <mxCell id="1" parent="0"/>\n'
        f"{body}\n"
        "      </root>\n"
        "    </mxGraphModel>\n"
        "  </diagram>\n"
        "</mxfile>\n"
    )
    OUT.write_text(xml, encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    gen_fig2()