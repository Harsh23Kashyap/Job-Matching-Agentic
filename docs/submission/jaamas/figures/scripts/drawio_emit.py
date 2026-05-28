"""Emit diagrams.net (draw.io) mxGraph XML — shared JAAMAS figure helpers."""
from __future__ import annotations

import textwrap
from pathlib import Path

PALETTE = {
    "actor_c": ("#eef2ff", "#4338ca"),
    "actor_e": ("#fffbeb", "#b45309"),
    "portal": ("#f8fafc", "#64748b"),
    "agent_c": ("#ecfdf5", "#047857"),
    "agent_e": ("#fff7ed", "#ea580c"),
    "broker": ("#eff6ff", "#2563eb"),
    "admin": ("#faf5ff", "#7c3aed"),
}

PAGE_BORDER_ID = "pageframe"
BORDER_INSET = 14
BORDER_STYLE = (
    "rounded=0;whiteSpace=wrap;html=1;fillColor=none;"
    "strokeColor=#94a3b8;strokeWidth=1.5;pointerEvents=0;"
)


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def bold_lines(header: str, *lines: str) -> str:
    body = "&lt;br&gt;".join(esc(x) for x in lines)
    return f"&lt;b&gt;{esc(header)}&lt;/b&gt;&lt;br&gt;{body}"


def box_style(fill: str, stroke: str, extra: str = "") -> str:
    base = (
        "rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
        "spacingTop=6;spacingBottom=6;fontSize=13;fontFamily=Helvetica;"
        f"fillColor={fill};strokeColor={stroke};strokeWidth=1.5;"
    )
    return base + extra


def edge_style(stroke: str = "#475569", dashed: bool = False) -> str:
    base = (
        "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;"
        "jettySize=auto;html=1;strokeWidth=1.5;"
        f"strokeColor={stroke};fontSize=11;fontColor=#334155;"
        "endArrow=blockThin;endFill=1;"
    )
    if dashed:
        base += "dashed=1;dashPattern=8 6;"
    return base


def cell_vertex(cid: str, value: str, x: float, y: float, w: float, h: float, style: str) -> str:
    return textwrap.dedent(
        f"""\
        <mxCell id="{cid}" value="{value}" style="{style}" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>"""
    )


def cell_edge(
    eid: str,
    source: str,
    target: str,
    label: str = "",
    dashed: bool = False,
    stroke: str = "#475569",
    *,
    exit_x: float | None = None,
    exit_y: float | None = None,
    entry_x: float | None = None,
    entry_y: float | None = None,
) -> str:
    lab = f' value="{esc(label)}"' if label else ""
    ports = ""
    if exit_x is not None:
        ports += f' exitX="{exit_x}" exitY="{exit_y}" exitDx="0" exitDy="0"'
    if entry_x is not None:
        ports += f' entryX="{entry_x}" entryY="{entry_y}" entryDx="0" entryDy="0"'
    return textwrap.dedent(
        f"""\
        <mxCell id="{eid}"{lab} style="{edge_style(stroke, dashed)}" edge="1" parent="1" source="{source}" target="{target}"{ports}>
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>"""
    )


def cell_edge_points(
    eid: str,
    source: str,
    target: str,
    points: list[tuple[float, float]],
    label: str = "",
    dashed: bool = False,
    stroke: str = "#475569",
    *,
    exit_x: float | None = None,
    exit_y: float | None = None,
    entry_x: float | None = None,
    entry_y: float | None = None,
) -> str:
    lab = f' value="{esc(label)}"' if label else ""
    ports = ""
    if exit_x is not None:
        ports += f' exitX="{exit_x}" exitY="{exit_y}" exitDx="0" exitDy="0"'
    if entry_x is not None:
        ports += f' entryX="{entry_x}" entryY="{entry_y}" entryDx="0" entryDy="0"'
    pts = "\n".join(f'            <mxPoint x="{x}" y="{y}" />' for x, y in points)
    points_xml = f"\n          <Array as=\"points\">\n{pts}\n          </Array>"
    return textwrap.dedent(
        f"""\
        <mxCell id="{eid}"{lab} style="{edge_style(stroke, dashed)}" edge="1" parent="1" source="{source}" target="{target}"{ports}>
          <mxGeometry relative="1" as="geometry">{points_xml}
          </mxGeometry>
        </mxCell>"""
    )


def page_border(page_w: float, page_h: float) -> str:
    inset = BORDER_INSET
    width, height = page_w - 2 * inset, page_h - 2 * inset
    return textwrap.dedent(
        f"""\
        <mxCell id="{PAGE_BORDER_ID}" parent="1" style="{BORDER_STYLE}" vertex="1" value="">
          <mxGeometry x="{inset}" y="{inset}" width="{width}" height="{height}" as="geometry"/>
        </mxCell>"""
    )


def write_mxfile(path: Path, diagram_id: str, page_w: float, page_h: float, cells: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    inner = "\n".join([page_border(page_w, page_h), *cells])
    text = f"""<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" agent="JobMatch-JAAMAS" version="24.0">
  <diagram id="{diagram_id}" name="{diagram_id}">
    <mxGraphModel background="#fafafa" dx="1200" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{page_w}" pageHeight="{page_h}" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{inner}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    path.write_text(text, encoding="utf-8")
