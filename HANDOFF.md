# Handoff
> Written: 2026-05-27 | Branch: main | Dir: /Users/harshkashyap/Projects/JobMatcher-v1/Job-Matching-Agentic

## Goal

Deliver a **thesis-ready JobMatch system**: three-agent product with role portals and composite matching **plus** a complete **offline research evaluation pipeline** (benchmarks, ablation, significance, fairness, explainability, paper tables) and a **manuscript draft** (`docs/research/RESEARCH-PAPER.md`) grounded only in generated reports under `backend/reports/`.

## Current state

- **Done:**
  - V1/V1.1 product: three agents, auth, portals, LLM resume/JD parse, composite scoring (40/30/15/10/5), drawer breakdown, demo seed, feedback, similar entities, resume coach
  - **Offline research stack** (`backend/benchmarks/`): comparison, ablation (9 variants), paired bootstrap significance, fairness audit (synthetic pairs), explainability eval, synthetic 100×50 corpus generator, paper table generators (MD/CSV/LaTeX)
  - **Full research pipeline** — `python backend/scripts/run_research_pipeline.py` → `backend/reports/research_run_<timestamp>/` (9 stages + manifest)
  - **Research archive export** — `bash scripts/run_research_suite.sh` → `docs/research/evaluation/`
  - **Manuscript draft** — `docs/research/RESEARCH-PAPER.md` synced from `research_run_smoke_test` + `cross_encoder_report.json`
  - Smoke pipeline run validated: `backend/reports/research_run_smoke_test/` (all steps OK, CE skipped)
  - Benchmark tests: **38 passed** in `tests/benchmarks/`
- **In progress:** Large **uncommitted** research + doc additions (see Environment); not pushed since thesis-demo commit `bfa27e1`.
- **Blocked:** None for local demo or offline eval.

## Decisions made

| Decision | Why | Alternatives rejected |
|----------|-----|----------------------|
| Single pipeline entry `backend/scripts/run_research_pipeline.py` | One timestamped run folder for paper reproducibility | Scattered shell scripts only |
| All pipeline outputs under `research_run_<timestamp>/` | Keeps paper tables + reports co-located | Flat `backend/reports/` overwrite |
| Cross-encoder optional in pipeline (`--enable-cross-encoder`) | CE adds ~141 ms/query and hurt nDCG on demo corpus | Always-on CE in pipeline |
| Fail-fast dataset validation (empty corpus = error) | Prevents silent zero-query benchmark runs | Warn-only on empty labels |
| Paper numbers only from `backend/reports/` | No hallucinated results in manuscript | Inline estimates in prose |
| Composite eval separate from ablation step | Production `compute_composite` vs component variants | Only ablation for composite |
| Significance reuses in-memory per-query (no re-run) | Saves ~4s per comparison bootstrap | Subprocess `run_significance` only |
| Fairness audit synthetic fixtures only | No real-user demographic inference | Production user audit |
| `research_run_smoke_test` as primary paper source | Latest full pipeline artifact set | Mixed root + run folder reports |
| Composite scoring default in production UI | Explainable multi-signal ranker for demo | Semantic-only cards |

## Open questions

- [ ] Hypothesis: 100×50 corpus (`data/research/`) will widen bootstrap CIs but confirm composite lead — run `run_research_pipeline.py --data-dir data/research --eval-path data/research/eval_pairs.json`
- [ ] Unknown: Whether cross-encoder should stay disabled permanently or needs domain-tuned model — evidence: nDCG Δ = −0.108 on demo corpus
- [ ] Hunch: Rules explainer low skill-mention rate (25.3%) hurts recruiter trust more than template hallucination flags — needs human eval
- [ ] Unknown: Why `demo.admin@test.com` 401 in some automated smoke runs — candidate/employer work
- [ ] Hypothesis: `AdminConsole.jsx` wrong `ResultsPanel` props — admin match UI may be empty
- [ ] Paper §3 architecture diagram — waiting on supervisor approval
- [ ] Should research modules be committed in one PR or split (product vs research)?

## Blockers & dependencies

| What | Who/Where | Status |
|------|-----------|--------|
| Git commit + push of research stack | User | **not done** — large untracked tree |
| Ollama for LLM explain/parse | Local dev | optional — template fallback works |
| Cross-encoder in unified pipeline run | Dev | skipped in smoke test; report exists at `backend/reports/cross_encoder_report.json` |
| 100×50 eval run | Dev | corpus generated; pipeline not run at scale |

## Environment

- **Branch:** `main` (last pushed commit `bfa27e1`; **many uncommitted changes**)
- **Uncommitted changes:** ~17 modified + ~90 untracked files (benchmarks, research docs, scripts, tests, `docs/research/RESEARCH-PAPER.md`, `backend/scripts/`, `data/research/`, `data/fairness_audit_profiles.json`)
- **Recent commits (on remote):**
  - `bfa27e1` Add composite scoring, portal polish, and candidate flow fixes for thesis demo
  - `0185fa8` Polish employer portal, demo seed, and shared portal UX for thesis demo
  - `517b099` Polish candidate profile UX and jobs results for thesis demo
- **Build status:** passing (`npm run build` — last verified at thesis-demo push)
- **Test status:** `tests/benchmarks/` **38 passed**; full suite count not re-run this session — run `pytest ../tests -q` before commit
- **Active processes:** None assumed; backend `:8001`, frontend `:5173` if demo running

## What worked

- `python backend/scripts/run_research_pipeline.py --skip-cross-encoder --run-id research_run_smoke_test` — ~12s, all 9 stages OK
- `generate_all_paper_tables()` → copy-paste LaTeX booktabs with `\label{tab:...}`
- Paired bootstrap significance: multimodal p=0.013, full composite vs semantic-only p=0.019 (nDCG@5)
- Dataset validation catches empty corpus before expensive embedding runs
- `git commit -m "single line"` — reliable in agent shell (HEREDOC hangs)

## What didn't work

- HEREDOC `git commit` in agent shell — hung 3+ minutes; use single `-m` line
- Cross-encoder reranking on composite — nDCG **degrades** (−0.108) with +141 ms/query; not production default
- RRF over single-component rankers in ablation — nDCG 0.564 vs full composite 0.942
- Browser automation on demo login buttons — stale refs; use API smoke or manual demo
- `@jobmatch.test` email in register smoke — pydantic rejects reserved TLD

## Commands

```bash
# Full offline research pipeline (primary)
python backend/scripts/run_research_pipeline.py
python backend/scripts/run_research_pipeline.py --skip-cross-encoder --run-id my_run
python backend/scripts/run_research_pipeline.py --enable-cross-encoder

# Export to docs/research/evaluation/
bash scripts/run_research_suite.sh
bash scripts/run_research_suite.sh --from-cache

# Individual stages (write to backend/reports/ by default)
cd backend && source .venv/bin/activate
python -m benchmarks.run_comparison
python -m benchmarks.run_ablation
python -m benchmarks.run_significance
python -m benchmarks.run_fairness_audit
python -m benchmarks.run_explainability_eval
python -m benchmarks.run_paper_tables
python -m benchmarks.run_generate_research_dataset

# Benchmark tests
pytest ../tests/benchmarks -q

# Product demo
uvicorn main:create_app --factory --reload --port 8001   # from backend/
cd frontend && npm run dev

# Full test suite
cd backend && pytest ../tests -q
node --test tests/unit/test_*.mjs

# Demo logins (password: demo1234)
# demo.candidate@test.com | demo.employer@test.com | demo.admin@test.com
```

## Key files

| File | Why It Matters |
|------|---------------|
| `backend/scripts/run_research_pipeline.py` | **Single-command** research pipeline CLI |
| `backend/benchmarks/research_pipeline.py` | Orchestrates 9 evaluation stages |
| `backend/benchmarks/dataset_validation.py` | Corpus preflight checks |
| `backend/benchmarks/composite_eval.py` | Production composite offline eval |
| `backend/benchmarks/comparison.py` | Lexical vs embedding baselines |
| `backend/benchmarks/ablation.py` | Nine-variant component ablation |
| `backend/benchmarks/significance.py` | Paired bootstrap nDCG/MRR |
| `backend/benchmarks/fairness_audit.py` | Synthetic counterfactual audit |
| `backend/benchmarks/explainability_eval.py` | Explanation quality checks |
| `backend/benchmarks/paper_tables/generators.py` | Paper-ready MD/CSV/LaTeX tables |
| `backend/benchmarks/research_export.py` | Bundle → `docs/research/evaluation/` |
| `backend/core/scoring.py` | `compute_composite()` + weights |
| `docs/research/RESEARCH-PAPER.md` | **Manuscript draft** (report-backed numbers) |
| `docs/research/evaluation/` | Methodology, studies, artifacts, paper_tables |
| `backend/reports/research_run_smoke_test/` | Latest full pipeline outputs + paper tables |
| `backend/reports/cross_encoder_report.json` | CE quality/latency (separate from smoke run) |
| `data/eval_pairs.json` | Demo eval corpus (30 queries, 47 pairs) |
| `data/research/` | Generated 100×50 research corpus (not yet evaluated) |
| `data/fairness_audit_profiles.json` | 10 synthetic counterfactual pairs |
| `scripts/run_research_pipeline.sh` | Shell wrapper for pipeline |
| `tests/benchmarks/test_research_pipeline.py` | Pipeline validation-failure test |

## External links

None.

## Memory snapshot

None directly relevant.

## Persistent context

- Knowledge graph: `.claude/knowledge_graph.md`
- Design specs: `docs/design/HLD-multi-agent-system.md`, `docs/design/SDD-multi-agent-system.md`, `docs/design/V1-V2-SCOPE.md`
- Research: `docs/research/README.md`, `docs/research/RESEARCH-PAPER.md`, `docs/research/evaluation/FINDINGS.md`
- Demo: `docs/demo/DEMO-SCRIPT.md`, `docs/demo/DEMO-CHECKLIST.md`
- Paper inventory: `docs/research/PAPER-FEATURES-INVENTORY.md`

## Next steps

1. **Commit research stack** — stage benchmarks, scripts, tests, `docs/research/`, `data/fairness_audit_profiles.json` (exclude `backend/reports/` runs if gitignored) — verify: `git status` clean after commit
2. **Run pipeline with cross-encoder** — `python backend/scripts/run_research_pipeline.py --enable-cross-encoder --run-id research_run_with_ce` — verify: `pipeline_manifest.json` shows CE step OK; update RESEARCH-PAPER.md CE section from that run
3. **Large-scale eval** — `python backend/scripts/run_research_pipeline.py --data-dir data/research --eval-path data/research/eval_pairs.json --run-id research_run_100x50` — verify: `dataset_validation.json` shows 100 candidates, 50 jobs
4. **Refresh manuscript** after new runs — only copy numbers from new `backend/reports/research_run_*/` — verify: no TODO sections remain for completed studies
5. **Live thesis demo dry-run** — `docs/demo/DEMO-CHECKLIST.md` — verify: composite drawer, JD paste, employer candidates flow
6. **Full pytest before push** — `pytest ../tests -q` — verify: no regressions vs 208 baseline
