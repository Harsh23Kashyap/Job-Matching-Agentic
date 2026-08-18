# REPRODUCTION_LOG

## 2026-08-17 — Environment build
- `python3.11 -m venv backend/.venv`; `pip install -r requirements-min.txt scikit-learn scipy matplotlib`.
- Result: exit 0. Imports verified: torch 2.13.0, sentence-transformers 5.1.2, chromadb 0.4.24, scikit-learn 1.9.0, scipy, numpy 1.26.4. **PASS — experiments runnable.**
- Note: `requirements-min.txt` pins fastapi/uvicorn/numpy 1.26.4/pydantic 2.9.2/sentence-transformers 5.1.2/chromadb 0.4.24/pytest/httpx/passlib/pdfplumber/tiktoken/qdrant-client. sklearn/scipy/matplotlib are NOT pinned in the repo (added ad-hoc) → must be added to a pinned requirements file (repro gap).
- Constraint: `pdflatex` absent → LaTeX PDF compilation not reproducible here (user blocker).

## PENDING — EXP-011: reproduce baseline numbers in clean venv
- Plan: run `benchmarks.composite_eval`, `benchmarks.extended_evaluation`, compare to `research/audit/baseline/` snapshot; record any drift (embedding model version can shift cosine → nDCG).
- Acceptance: composite nDCG@5 within ±0.005 of 0.949; held-out ECE within CI of 0.0192; artifacts byte-diffed where deterministic.
- **RESULT: PASS (2026-08-17).** Clean venv (`backend/.venv`, PYTHONHASHSEED=0); MiniLM downloaded fresh. Fresh re-run vs baseline snapshot — all core numbers match byte-for-byte:
  - kfold_cv composite nDCG@5: 0.949236 == 0.949236 MATCH
  - calibration_binary ECE/Brier: (0.019156, 0.092836) == baseline MATCH
  - xgb_ranker held-out nDCG@5: 0.916653 == 0.916653 MATCH
  - counterfactual_50 (recourse/demographic flagged, demo top1-stable): (12, 9, 0.96) == baseline MATCH
- Acceptance met (composite within ±0.005; ECE within CI). The honest held-out numbers are deterministic & reproducible.
- `scalability` step (step 7, duplicate-15-jobs) was killed: it pegged CPU (load avg ~6) and stalled the session; it is non-defensible per the audit and will be replaced by a real latency/scale study (Phase 19/21). Its output was never required for verification. 6/7 artifacts valid JSON post-kill.

## 2026-08-17 — Phase 25/26: one-command runner (audit H9)
- Added `scripts/reproduce_all.sh` (bash -n OK): runs `benchmarks/extended_evaluation.py` (deterministic core) + EXP-012/013/014a/014b/015/019/020 + `verify_checks.py`, all with `PYTHONHASHSEED=0`. Regenerates `backend/reports/extended_evaluation/*.json` + `research/results/*.json`.
- Guarded `extended_evaluation.py` scalability step behind `RUN_SCALABILITY=1` (default OFF) so `main()` no longer hangs; import verified OK.
- EXP-018 (LLM labels via `claude -p`) is intentionally OUTSIDE the deterministic core (non-deterministic LLM annotator; documented separately).
- NOT yet executed end-to-end from a clean clone (that is the Phase-25 fresh-repro test, pending). Each sub-experiment has been run and verified individually.

## 2026-08-17 — threading hang + fix (watchdog)
- Under sustained external machine load (~7–10), fresh torch/sentence-transformers processes **blocked at 0.0% CPU on startup** (empty output, elapsed climbing) — a torch/tokenizers thread-contention hang, NOT slowness. Two runs (full extended_evaluation re-run; cold_start regen) hung this way and were killed by the watchdog.
- **Fix:** run single-threaded — `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false`. cold_start then completed immediately. Added these to `scripts/reproduce_all.sh`. Recommend the same env for all experiment runs on a loaded machine.
- **RQ6 (EXP-007) regenerated** with corpus-hitting synonym/misspelling maps + propagation verified (synonym folds to canonical → Δ=0 composite; misspelling shifts composite −0.078/pair but not top-5 rank).

## 2026-08-17 — Phase 23 path scrub (audit H5) + PDF toolchain
- Scrubbed hardcoded `/home/user/...` absolute paths from the 9 RELEASED evaluation artifacts (`docs/research/evaluation/artifacts/**` + `paper_tables/manifest.json`) → repo-relative; JSON validity preserved; results/numbers untouched. `docs/research/evaluation/` now free of the author-path leak.
- **Deliberately NOT scrubbed (flagged for a pre-release/anonymity pass):** (a) `research/audit/baseline/*` — frozen original snapshot, must keep as-is; (b) test fixtures `tests/unit/backend/test_contact_extract.py`, `test_resume_clean.py`, `tests/integration/test_feature_reverification.py` — embed the author's real GitHub/LeetCode handle as TEST DATA; scrubbing changes assertions → do with test updates; (c) internal `HANDOFF.md`, `VENUE-PLAN.md`, `*.log` — not part of the released submission artifact.
- **PDF toolchain:** TinyTeX (userspace) installed; `docs/submission/eswa/manuscript/main.tex` compiles (36 pp, 0 errors); PDF placeholder-scan PASS.

## 2026-08-18 — Stage-3 anonymity pass (completes the flagged 2026-08-17 item) + graded-channel run
- **Anonymity pass DONE (was "deliberately NOT scrubbed"):** replaced the author's real identity with a neutral placeholder ("Jordan Rivera" / jordan@example.com / linkedin.com/in/jordan / jordan.dev) across ALL released test fixtures: `tests/unit/backend/{test_contact_extract,test_resume_clean,test_resume_structured_extract,test_profile_quality}.py`, `tests/unit/frontend/{test_profile_fields,test_profile_normalize}.mjs`, `tests/integration/{test_feature_reverification,test_resume_upload,test_profile_quality_api}.py`. Inputs and assertions updated together; re-ran the suites (60 backend + 10 frontend) — all green. Removed the stale root `main.log` (leaked `/Users/harshkashyap/...`). Repo-wide sweep of `tests/` for the author identity now returns 0.
- **Reviewer-bundle documentation anonymization — now a RUNNABLE procedure (not a manual note):** `scripts/anonymize_reviewer_bundle.py` writes scrubbed copies of `README.md` + `docs/design/{HLD,SDD,V1-V2-SCOPE}.md` into `build/anon/` (replacing author names, supervisor, institution, GitHub URL, and LinkedIn with anonymized placeholders) and then VERIFIES zero residual identifier — run + verified clean 2026-08-18 (exit 0). The working tree is never mutated, so real attribution is preserved for the public release on acceptance. This backs the Data Availability claim that documentation is anonymized in the reviewer bundle. NOTE: `docs/submission/eswa/{title-page.tex, cover-letter.md, SUBMISSION-FORM-GUIDE.md}` legitimately carry author identity — they are the NON-anonymous title page / cover letter / submission-form parts, not the double-blind manuscript. `archive/` and `docs/submission/{jaamas,iui2027}/` are OTHER submissions. The 30 demo-corpus resume names in `data/cvs.json` are generic pseudonyms that feed the frozen embeddings; they do not link to the author and are left unchanged to preserve reproducibility of every reported number.
- **EXP-043/044 graded skill channel (prospective real-corpus run):** run ONCE per PROTOCOL.md §29 with the frozen graded matcher; three pre-specified variants (jaccard / exact-coverage / graded), NO credit-weight sweep on the real corpus (synthetic-dev only); weights UNCHANGED. Rationale: isolate the relation-aware novelty from the coverage-form change (hostile-review requirement). Artifact: `research/results/graded_skill_channel.json`.
