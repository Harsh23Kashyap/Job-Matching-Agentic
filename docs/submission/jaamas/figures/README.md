# JAAMAS paper figures

Academic grayscale diagrams for the multi-agent recruitment platform paper.

## Section mapping

| PDF | Section | Purpose |
|-----|---------|---------|
| `Fig1.pdf` | §3 Architecture | **Multi-agent system**: Candidate agent, Employer agent, Matchmaking agent, event bus, vector store, role portals |
| `Fig2.pdf` | §3 Architecture | Candidate workflow (pain point → agent → explained matches) |
| `Fig3.pdf` | §3 Architecture | Employer workflow |
| `Fig4.pdf` | §4 Implementation | Matching pipeline modules (retrieval, scoring, fusion, explainability) |
| `Fig5.pdf` | §5 Quality Metrics | Evaluation pipeline (corpus → drivers → metrics → regression) |

## Fig1 multi-agent diagram plan (draw.io)

Layout in `source/Fig1.drawio` (regenerate via `generate_jaamas_figures.py`):

```
[ UI / Application Layer: Candidate Portal | Employer Portal | Admin/Evaluation ]

[ Candidate Agent ]     [ Employer Agent ]     [ Matchmaking Agent (read-only) ]
  Resume/CV Input         JD Input               Read Candidate Store  <--+
  Resume Parsing          JD Parsing             Read Job Store        <--+
  Embedding Gen           Embedding Gen          Semantic Search
  Candidate Vector Store  Job Vector Store       Similarity Score
  Candidate Profile/State Job Profile/State      Ranked Recommendations --> portals

[ Shared Communication & State: Events | Snapshots/Contracts | Cache invalidation ]
```

Visual rules: grayscale only; solid arrows = owned write/processing path; dashed = read, query, or event.

## Regenerate

```bash
python3 scripts/generate_jaamas_figures.py
```

Requires draw.io CLI (`drawio`) on PATH.

## Known issue

~~Fig1 and Fig4 exports may produce very short PDF bounding boxes when using `--crop`.~~
Export script uses full page bounds (`-b 10` without `--crop`). Re-run `generate_jaamas_figures.py` after editing draw.io sources.

## LaTeX

Figures use `\JFig{../figures/FigN.pdf}` and labels `fig:1` … `fig:5`.
Cite in prose before each `\begin{JFigure}`.
