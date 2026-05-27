#!/usr/bin/env python3
"""Generate draw.io source diagrams for JAAMAS paper figures (academic greyscale style)."""

from __future__ import annotations

import html
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FIG_DIR = REPO / "docs/submission/jaamas/figures"
SRC_DIR = FIG_DIR / "source"

# Academic palette — readable in grayscale
FILL = "#f5f5f5"
FILL_DARK = "#e8e8e8"
FILL_STORE = "#ededed"
STROKE = "#333333"
FONT = "#1a1a1a"
FONT_SIZE = 11
TITLE_SIZE = 13

BOX_tpl = (
    "rounded=0;whiteSpace=wrap;html=1;"
    "fillColor={fill};strokeColor={stroke};fontColor={font};"
    "fontSize={size};align=center;verticalAlign=middle;"
)
EDGE_tpl = (
    "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
    "html=1;strokeColor={stroke};strokeWidth=1;endArrow=block;endFill=1;"
    "fontColor={font};fontSize=10;"
)


def _style(template: str, *, fill: str = FILL, size: int = FONT_SIZE, dashed: bool = False) -> str:
    s = template.format(fill=fill, stroke=STROKE, font=FONT, size=size)
    if dashed:
        s += "dashed=1;"
    return s


def _label(text: str) -> str:
    return "<br>".join(html.escape(part) for part in text.split("\n"))


class DrawioBuilder:
    def __init__(self, page_width: int = 1100, page_height: int = 780) -> None:
        self.page_width = page_width
        self.page_height = page_height
        self._id = 2
        self.cells: list[str] = []

    def _next_id(self) -> str:
        cid = str(self._id)
        self._id += 1
        return cid

    def box(
        self,
        label: str,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        fill: str = FILL,
        size: int = FONT_SIZE,
        bold: bool = False,
    ) -> str:
        cid = self._next_id()
        text = _label(label)
        if bold:
            fill = FILL_DARK
        st = _style(BOX_tpl, fill=fill, size=size)
        self.cells.append(
            f'        <mxCell id="{cid}" value="{text}" style="{st}" vertex="1" parent="1">\n'
            f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>\n'
            f"        </mxCell>"
        )
        return cid

    def edge(
        self,
        source: str,
        target: str,
        *,
        label: str = "",
        dashed: bool = False,
        exit_x: float | None = None,
        exit_y: float | None = None,
        entry_x: float | None = None,
        entry_y: float | None = None,
    ) -> None:
        cid = self._next_id()
        st = _style(EDGE_tpl, dashed=dashed)
        lbl = _label(label) if label else ""
        attrs = ""
        if exit_x is not None:
            attrs += f' exitX="{exit_x}" exitY="{exit_y}"'
        if entry_x is not None:
            attrs += f' entryX="{entry_x}" entryY="{entry_y}"'
        self.cells.append(
            f'        <mxCell id="{cid}" value="{lbl}" style="{st}" edge="1" parent="1" '
            f'source="{source}" target="{target}"{attrs}>\n'
            f'          <mxGeometry relative="1" as="geometry"/>\n'
            f"        </mxCell>"
        )

    def title(self, text: str) -> None:
        self.box(text, 20, 12, self.page_width - 40, 28, fill=FILL_DARK, size=TITLE_SIZE, bold=True)

    def build(self, diagram_name: str) -> str:
        body = "\n".join(self.cells)
        return f"""<mxfile host="app.diagrams.net" modified="2026-05-27T00:00:00.000Z" agent="generate_jaamas_figures.py" version="22.1.0">
  <diagram name="{diagram_name}" id="{diagram_name}">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.page_width}" pageHeight="{self.page_height}" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""


def fig1_platform() -> str:
    """Multi-agent architecture: three agent pipelines, UI layer, shared communication."""
    b = DrawioBuilder(page_width=1200, page_height=780)
    b.title("Fig. 1  Multi-agent architecture of the JobMatch recruitment system")

    # --- UI / Application Layer ---
    b.box("UI / Application Layer", 40, 48, 1120, 26, fill=FILL_DARK, size=12, bold=True)
    cand_port = b.box("Candidate\nPortal", 90, 82, 150, 50)
    emp_port = b.box("Employer\nPortal", 525, 82, 150, 50)
    admin = b.box("Admin /\nEvaluation View", 960, 82, 150, 50)

    col_w, box_w, box_h, step_gap = 300, 260, 40, 46
    x_ca, x_ea, x_ma = 40, 430, 820
    y0 = 158

    def pipeline_column(title: str, x: float, steps: list[str]) -> list[str]:
        b.box(title, x, y0, col_w, 30, fill=FILL_DARK, bold=True)
        ids: list[str] = []
        y = y0 + 38
        for step in steps:
            fill = FILL_STORE if "Vector Store" in step else FILL
            ids.append(b.box(step, x + 20, y, box_w, box_h, fill=fill))
            y += step_gap
        return ids

    ca = pipeline_column(
        "Candidate Agent",
        x_ca,
        [
            "Resume / CV Input",
            "Resume Parsing",
            "Embedding Generation",
            "Candidate Vector Store",
            "Candidate Profile / State",
        ],
    )
    ea = pipeline_column(
        "Employer Agent",
        x_ea,
        [
            "Job Description Input",
            "JD Parsing",
            "Embedding Generation",
            "Job Vector Store",
            "Job Profile / State",
        ],
    )
    ma = pipeline_column(
        "Matchmaking Agent  (read-only)",
        x_ma,
        [
            "Read Candidate Store",
            "Read Job Store",
            "Semantic Search",
            "Similarity / Matching Score",
            "Ranked Recommendations",
        ],
    )

    # --- Shared communication & state ---
    y_shared = 430
    b.box("Shared Communication & State Layer", 40, y_shared, 1120, 26, fill=FILL_DARK, size=12, bold=True)
    events = b.box(
        "Agent Messages / Events\n(profile updated · job updated · match completed)",
        60,
        y_shared + 34,
        340,
        52,
    )
    snaps = b.box(
        "Shared Contracts & Snapshots\n(canonical skills · versioned match inputs)",
        430,
        y_shared + 34,
        340,
        52,
    )
    notify = b.box(
        "State Update Notifications\n(match cache invalidation)",
        800,
        y_shared + 34,
        340,
        52,
    )

    # --- Legend ---
    b.box(
        "Solid arrows: owned write / processing path   |   Dashed arrows: read, query, or event",
        120,
        y_shared + 100,
        960,
        28,
        fill=FILL_DARK,
        size=10,
    )

    # UI -> agent inputs
    b.edge(cand_port, ca[0], exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0, label="upload / edit")
    b.edge(emp_port, ea[0], exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0, label="post / edit")
    b.edge(admin, notify, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0, dashed=True, label="monitor")

    # Vertical pipelines (owning agent)
    for ids in (ca, ea, ma):
        for i in range(len(ids) - 1):
            b.edge(ids[i], ids[i + 1], exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)

    # Vector stores -> matchmaking reads (dashed)
    b.edge(ca[3], ma[0], exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5, dashed=True, label="read")
    b.edge(ea[3], ma[1], exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5, dashed=True, label="read")

    # Ranked results -> portals
    b.edge(ma[4], cand_port, exit_x=0, exit_y=0.5, entry_x=1, entry_y=0.5, label="job matches")
    b.edge(ma[4], emp_port, exit_x=0, exit_y=0.5, entry_x=1, entry_y=0.5, label="candidate matches")

    # Profile/state -> shared layer
    b.edge(ca[4], snaps, exit_x=0.5, exit_y=1, entry_x=0.25, entry_y=0)
    b.edge(ea[4], snaps, exit_x=0.5, exit_y=1, entry_x=0.75, entry_y=0)
    b.edge(ca[4], events, exit_x=0, exit_y=0.5, entry_x=1, entry_y=0.5, dashed=True)
    b.edge(ea[4], events, exit_x=0, exit_y=0.5, entry_x=1, entry_y=0.5, dashed=True)

    # Events -> matchmaking invalidation
    b.edge(events, ma[2], exit_x=1, exit_y=0, entry_x=0, entry_y=1, dashed=True, label="refresh")
    b.edge(notify, ma[2], exit_x=0, exit_y=0, entry_x=1, entry_y=1, dashed=True)

    return b.build("Fig1")


def _sequence_fig(title: str, participants: list[str], steps: list[tuple[str, str, str]]) -> str:
    """Build a left-to-right sequence-style diagram using columns and numbered arrows."""
    b = DrawioBuilder(page_width=1100, page_height=720)
    b.title(title)

    n = len(participants)
    col_w = 130
    gap = (b.page_width - 80 - n * col_w) / max(n - 1, 1)
    x0 = 40
    tops: dict[str, str] = {}

    for i, name in enumerate(participants):
        x = x0 + i * (col_w + gap)
        tops[name] = b.box(name, x, 60, col_w, 48, bold=True)
        # lifeline
        b.box("", x + col_w / 2 - 1, 108, 2, 520, fill=STROKE)

    y = 130
    for idx, (src, msg, dst) in enumerate(steps, start=1):
        label = f"{idx}. {msg}"
        b.edge(tops[src], tops[dst], label=label, exit_x=1 if participants.index(dst) > participants.index(src) else 0, exit_y=0.5, entry_x=0 if participants.index(dst) > participants.index(src) else 1, entry_y=0.5)
        y += 50

    return b.build(title.split()[1])


def fig2_candidate_workflow() -> str:
    parts = ["Candidate", "Parser", "Candidate\nAgent", "Matchmaking\nAgent", "Matching\nCore", "Portal"]
    steps = [
        ("Candidate", "Upload / edit resume", "Parser"),
        ("Parser", "Extract skills & fields", "Candidate\nAgent"),
        ("Candidate\nAgent", "Profile snapshot + embed", "Matchmaking\nAgent"),
        ("Matchmaking\nAgent", "Retrieve jobs", "Matching\nCore"),
        ("Matching\nCore", "Score · fuse · explain", "Matchmaking\nAgent"),
        ("Matchmaking\nAgent", "Ranked matches", "Portal"),
        ("Portal", "View · save · apply", "Candidate"),
    ]
    return _sequence_fig("Fig. 2  Candidate workflow (profile to matches)", parts, steps)


def fig3_employer_workflow() -> str:
    parts = ["Employer", "Parser", "Employer\nAgent", "Matchmaking\nAgent", "Matching\nCore", "Portal"]
    steps = [
        ("Employer", "Upload / paste JD", "Parser"),
        ("Parser", "Extract requirements", "Employer\nAgent"),
        ("Employer\nAgent", "Job snapshot + embed", "Matchmaking\nAgent"),
        ("Matchmaking\nAgent", "Retrieve candidates", "Matching\nCore"),
        ("Matching\nCore", "Rank · constraints · fairness audit", "Matchmaking\nAgent"),
        ("Matchmaking\nAgent", "Shortlist + explanations", "Portal"),
        ("Portal", "Review · save · contact", "Employer"),
    ]
    return _sequence_fig("Fig. 3  Employer workflow (job posting to shortlist)", parts, steps)


def fig4_pipeline() -> str:
    b = DrawioBuilder(page_width=1200, page_height=420)
    b.title("Fig. 4  Matching pipeline (hybrid retrieval and scoring)")

    stages = [
        "Text\nnormalization",
        "Skill\nextraction",
        "Lexical\nretrieval",
        "Embedding\nretrieval",
        "Constraint\nscoring",
        "Fusion\n(RRF)",
        "Calibration\n(optional)",
        "Explanation",
    ]
    w, h, y = 118, 52, 120
    x0 = 30
    gap = 18
    ids: list[str] = []
    for i, label in enumerate(stages):
        x = x0 + i * (w + gap)
        style_fill = FILL_DARK if label.startswith("Calibration") else FILL
        ids.append(b.box(label, x, y, w, h, fill=style_fill))

    for i in range(len(ids) - 1):
        b.edge(ids[i], ids[i + 1], exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)

    b.box("Portal default: composite six-signal score merges semantic, skills, title, experience, compensation, remote", 120, 240, 960, 36, fill=FILL_STORE, size=10)
    b.box("Dashed path: feedback-aware boost when explicitly enabled on match request", 120, 290, 720, 32, fill=FILL_DARK, size=10)

    return b.build("Fig4")


def fig5_evaluation() -> str:
    b = DrawioBuilder(page_width=1200, page_height=420)
    b.title("Fig. 5  Offline evaluation pipeline")

    stages = [
        "Dataset\n(30 CV · 15 jobs)",
        "Labels\n(47 pairs)",
        "Negative\nmining",
        "Ranking\nruns",
        "Metrics\nP@K · R@K · nDCG@K",
        "Fairness\naudit",
        "Regression\n& paper tables",
    ]
    w, h, y = 130, 52, 120
    x0 = 30
    gap = 20
    ids: list[str] = []
    for label in stages:
        x = x0 + len(ids) * (w + gap)
        ids.append(b.box(label, x, y, w, h, fill=FILL_STORE if "Dataset" in label else FILL))

    for i in range(len(ids) - 1):
        b.edge(ids[i], ids[i + 1], exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)

    b.box("Driver: run_research_pipeline.py  ->  reports/research_run_TIMESTAMP/", 80, 240, 1040, 36, fill=FILL_DARK, size=10)
    b.box("Outputs: comparison, ablation, significance, fairness, explainability, LaTeX tables", 80, 290, 800, 32, fill=FILL_DARK, size=10)

    return b.build("Fig5")


FIGURES = {
    "Fig1": fig1_platform,
    "Fig2": fig2_candidate_workflow,
    "Fig3": fig3_employer_workflow,
    "Fig4": fig4_pipeline,
    "Fig5": fig5_evaluation,
}


def write_sources() -> list[Path]:
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for name, builder in FIGURES.items():
        path = SRC_DIR / f"{name}.drawio"
        path.write_text(builder(), encoding="utf-8")
        paths.append(path)
        print(f"Wrote {path}")
    return paths


def export_pdfs(sources: list[Path]) -> None:
    import shutil

    drawio = shutil.which("drawio") or "/opt/homebrew/bin/drawio"
    if not Path(drawio).is_file():
        raise FileNotFoundError("draw.io CLI not found; install from https://www.drawio.com/")
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    for src in sources:
        out = FIG_DIR / f"{src.stem}.pdf"
        cmd = [drawio, "-x", "-f", "pdf", "-o", str(out), str(src), "-b", "10"]
        print("Export:", " ".join(cmd))
        subprocess.run(cmd, check=True)
        if not out.is_file() or out.stat().st_size == 0:
            raise RuntimeError(f"Export failed: {out} was not created")
        print(f"Exported {out} ({out.stat().st_size // 1024} KB)")


def write_mermaid_alternates() -> None:
    """Lightweight Mermaid sources for quick edits (not exported to PDF)."""
    mmd = {
        "Fig1": """flowchart TB
  subgraph ui [UI / Application Layer]
    CP[Candidate Portal]
    EP[Employer Portal]
    AD[Admin / Evaluation View]
  end
  subgraph ca [Candidate Agent]
    CV[Resume / CV Input] --> RP[Resume Parsing] --> CE[Embedding Generation]
    CE --> CVS[(Candidate Vector Store)] --> CPS[Candidate Profile / State]
  end
  subgraph ea [Employer Agent]
    JD[Job Description Input] --> JP[JD Parsing] --> JE[Embedding Generation]
    JE --> JVS[(Job Vector Store)] --> JPS[Job Profile / State]
  end
  subgraph ma [Matchmaking Agent]
    RC[Read Candidate Store] --> RS[Read Job Store] --> SS[Semantic Search]
    SS --> SC[Similarity / Matching Score] --> RR[Ranked Recommendations]
  end
  subgraph shared [Shared Communication and State]
    EV[Agent Messages / Events]
    SN[Shared Contracts and Snapshots]
    NT[State Update Notifications]
  end
  CP --> CV
  EP --> JD
  AD -.-> NT
  CVS -. read .-> RC
  JVS -. read .-> RS
  RR --> CP
  RR --> EP
  CPS --> SN
  JPS --> SN
  CPS -.-> EV
  JPS -.-> EV
  EV -. refresh .-> SS
""",
        "Fig2": """sequenceDiagram
  participant C as Candidate
  participant P as Parser
  participant CA as Candidate Agent
  participant MA as Matchmaking Agent
  participant MC as Matching Core
  participant UI as Portal
  C->>P: Upload / edit resume
  P->>CA: Extracted fields
  CA->>MA: Profile snapshot
  MA->>MC: Retrieve jobs
  MC->>MA: Scores + explanations
  MA->>UI: Ranked matches
  UI->>C: Save / apply
""",
        "Fig3": """sequenceDiagram
  participant E as Employer
  participant P as Parser
  participant EA as Employer Agent
  participant MA as Matchmaking Agent
  participant MC as Matching Core
  participant UI as Portal
  E->>P: Upload / paste JD
  P->>EA: Extracted requirements
  EA->>MA: Job snapshot
  MA->>MC: Retrieve candidates
  MC->>MA: Rank + fairness flags
  MA->>UI: Shortlist
  UI->>E: Save / contact
""",
        "Fig4": """flowchart LR
  A[Text normalization] --> B[Skill extraction]
  B --> C[Lexical retrieval]
  C --> D[Embedding retrieval]
  D --> E[Constraint scoring]
  E --> F[Fusion RRF]
  F --> G[Calibration]
  G --> H[Explanation]
""",
        "Fig5": """flowchart LR
  A[Dataset] --> B[Labels]
  B --> C[Negative mining]
  C --> D[Ranking runs]
  D --> E[Metrics]
  E --> F[Fairness audit]
  F --> G[Regression tests]
""",
    }
    for name, content in mmd.items():
        path = SRC_DIR / f"{name}.mmd"
        path.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"Wrote {path}")


def main() -> int:
    sources = write_sources()
    write_mermaid_alternates()
    try:
        export_pdfs(sources)
    except subprocess.CalledProcessError as exc:
        print("PDF export failed:", exc, file=sys.stderr)
        print("Draw.io sources are in:", SRC_DIR, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
