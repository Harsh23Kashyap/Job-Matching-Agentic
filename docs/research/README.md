# Research documentation

Thesis and paper artifacts for JobMatch offline evaluation.

## Evaluation archive (primary)

**[evaluation/](evaluation/)** · complete research bundle:

- Methodology (corpus, metrics, bootstrap testing)
- Six study write-ups with tables
- Raw JSON/CSV artifacts per run
- Unified paper tables (`artifacts/tables/`)
- Synthesis in [FINDINGS.md](evaluation/FINDINGS.md)

```bash
bash scripts/run_research_suite.sh              # run all + export
bash scripts/run_research_suite.sh --from-cache # export existing reports
```

## Other research docs

| Doc | Purpose |
|-----|---------|
| **[RESEARCH-PAPER.md](RESEARCH-PAPER.md)** | **Manuscript draft** · architecture, methods, results from `backend/reports/` |
| [PAPER-FEATURES-INVENTORY.md](PAPER-FEATURES-INVENTORY.md) | Feature ↔ paper section mapping |
| [../design/V1-V2-SCOPE.md](../design/V1-V2-SCOPE.md) | Scope and benchmark requirements |

## Live report staging

Ephemeral runs land in `backend/reports/` (gitignored). The research suite copies them into `docs/research/evaluation/artifacts/runs/` for version control.
