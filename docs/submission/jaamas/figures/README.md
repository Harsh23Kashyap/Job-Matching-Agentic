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

Recommended layout for `source/Fig1.drawio` re-export:

```
[Candidate Portal]     [Employer Portal]     [Admin Portal]
        |                      |                    |
        v                      v                    v
              [ FastAPI Gateway / Auth ]
                        |
        +---------------+---------------+
        v               v               v
 [Candidate Agent] [Employer Agent] [Matchmaking Agent]
   owns CV state     owns job state    read-only scoring
        |               |               ^
        |  embed/upsert |  embed/upsert |
        v               v               |
      [ Vector Store (Chroma/Qdrant) ]--+
        |
 [ Event Bus: ProfileUpdated / JobUpdated ]
        |
 [ SQLite: auth, feedback, activity ]
```

Visual rules: grayscale only; solid arrows = write path (owning agent); dashed = read/query; double-line box around Matchmaking agent labeled ``read-only''.

## Regenerate

```bash
python3 scripts/generate_jaamas_figures.py
```

Requires draw.io CLI (`drawio`) on PATH.

## Known issue

Fig1 and Fig4 exports may produce very short PDF bounding boxes.
Re-export with full canvas crop before submission.

## LaTeX

Figures use `\JFig{../figures/FigN.pdf}` and labels `fig:1` … `fig:5`.
Cite in prose before each `\begin{JFigure}`.
