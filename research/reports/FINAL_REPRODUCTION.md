# FINAL_REPRODUCTION (2026-08-18)

## One-command reproduction
`bash scripts/reproduce_all.sh` (from repo root) regenerates every `backend/reports/extended_evaluation/*.json`
and `research/results/*.json` artifact, then auto-generates the manuscript tables and runs the numerical
verifier as a gate. Environment is pinned deterministic:
`PYTHONHASHSEED=0 PYTHONPATH=. OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false`, every
script seeds 42. Dependencies: `backend/requirements-min.txt` + `backend/requirements-research.txt`
(scikit-learn 1.9.0, scipy 1.17.1, xgboost 3.2.0, matplotlib) — the two BLOCKER dependency gaps found in
code review are now declared.

Coverage (code-review fix): reproduce_all.sh now runs EXP-011,012,013,014a/b,015,019,020,022, then the
Stage-2 set EXP-023 (synthetic gen — runs FIRST since EXP-024/030 read it),024,025,026,027,028,029,030,033,
then the table generator (§AA) and `verify_paper_numbers.py` (§AB). Scalability (EXP-031/032) stays opt-in
(`RUN_SCALABILITY=1`) as a long micro-benchmark; EXP-018 (LLM-assisted labels) is separate (needs `claude -p`).

## Determinism verified
- Ran `generalization.py` twice → outputs **byte-identical** (`diff` clean). Seeds + single-thread env make
  numeric/tokenizer stacks deterministic; the earlier torch-hang-under-load risk is mitigated by the env.
- `bash -n scripts/reproduce_all.sh` → syntax OK.
- The banned `hash()`-based seeding (audit B3) was re-introduced in `robustness_matrix.py` and has been
  replaced with a sha256 `_stable_offset` (reproducible across processes); re-run reproduces prior values.

## Toolchain
- PDF: TinyTeX (userspace) `pdflatex` → `main.pdf` compiles clean, **39 pages, 0 errors, 0 undefined refs**.
- Tests: `pytest tests/unit/backend/test_scientific_claims.py` → 9/9 pass (adds the non-finite-embedding guard).

## Known reproduction caveats (honest)
- Full `reproduce_all.sh` takes ~15–25 min on CPU (embedding + bootstraps); the synthetic structure-recovery
  embeds 575 texts and the model-selection search fits ~25 configs across 5 folds.
- Numbers are hardware-CPU deterministic; a different BLAS/threading config could shift the last digit of a
  bootstrap CI bound (means/point estimates are stable). Percentile latencies are machine-dependent.
- No git operations are performed (repo constraint); "fresh clone" reproduction is emulated by the clean,
  seed-pinned re-runs above rather than an actual `git clone`.
