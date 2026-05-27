# JobMatch Offline Evaluation · Research Archive

Paper- and thesis-ready evaluation bundle for the JobMatch multi-agent matching system.

## Quick start

```bash
# Full offline pipeline (all 9 stages, one timestamped folder)
python backend/scripts/run_research_pipeline.py
# → backend/reports/research_run_<timestamp>/

# Run all studies + export (from repo root)
bash scripts/run_research_suite.sh

# Export existing backend/reports without re-running (~instant)
bash scripts/run_research_suite.sh --from-cache
```

## Folder layout

```
evaluation/
├── README.md                 ← you are here
├── FINDINGS.md               ← synthesis (auto-generated each export)
├── methodology/              ← fixed protocol documentation
│   ├── corpus-and-labels.md
│   ├── metrics-and-protocols.md
│   └── statistical-testing.md
├── studies/                  ← per-study write-ups (auto-generated)
│   └── …
├── paper_tables/             ← manuscript tables (Markdown/CSV/LaTeX)
│   ├── table1_method_comparison.*
│   └── …
└── artifacts/
    ├── manifest.json
    ├── latest/
    └── tables/
```

## Paper tables (manuscript)

```bash
bash scripts/generate_paper_tables.sh
# → docs/research/evaluation/paper_tables/
```

Six tables with `\label{tab:...}` for LaTeX: method comparison, ablation, latency, fairness, explanation quality, qualitative examples.

## Studies included

| # | Study | Driver | Key question |
|---|-------|--------|--------------|
| 1 | Embedding strategies | `run_eval` | Which dense retrieval signal works best? |
| 2 | Lexical vs embedding | `run_comparison` | Do BM25/TF-IDF beat embeddings? |
| 3 | Composite ablation | `run_ablation` | Which production score components matter? |
| 4a | Significance (embedding) | `run_significance` | Are gains over semantic statistically significant? |
| 4b | Significance (ablation) | `run_significance --source ablation` | Do composite additions beat semantic-only? |
| 5 | Cross-encoder | `run_cross_encoder_report` | Quality/latency trade-off of CE rerank |

## Corpus

- **30** candidate profiles (`data/cvs.json`)
- **15** job postings (`data/jobs.json`)
- **30** labeled queries, **47** graded pairs (`data/eval_pairs.json`)
- Relevance grades **0–2** (binary relevant = grade > 0)

## Production vs research

| Aspect | Production portals | Research benchmarks |
|--------|-------------------|---------------------|
| Default strategy | `composite` (40/30/15/10/5) | Varies by study |
| Retrieval | ANN (Chroma/Qdrant) | Exhaustive (all 15 jobs) |
| Cross-encoder | Off by default | Opt-in report only |
| Lexical baselines | Not in API | Offline only |

## Regenerating

```bash
cd backend && source .venv/bin/activate

# Individual studies → backend/reports/
python -m benchmarks.run_eval
python -m benchmarks.run_comparison
python -m benchmarks.run_ablation
python -m benchmarks.run_significance
python -m benchmarks.run_significance --source ablation --baseline semantic_only --prefix significance_ablation
ENABLE_CROSS_ENCODER_RERANK=true python -m benchmarks.run_cross_encoder_report

# Full export
python -m benchmarks.run_research_suite --from-cache
```

## Related docs

- [PAPER-FEATURES-INVENTORY.md](../PAPER-FEATURES-INVENTORY.md) · feature ↔ paper mapping
- [backend/benchmarks/README.md](../../backend/benchmarks/README.md) · driver reference
- [data/README.md](../../data/README.md) · corpus files
