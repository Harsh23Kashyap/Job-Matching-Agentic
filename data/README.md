# Data

Evaluation corpus and benchmark artifacts. Loaded on backend startup by `bootstrap.py`.

## Corpus files

| File | Contents |
|------|----------|
| `cvs.json` | 30 structured candidate profiles |
| `jobs.json` | 15 structured job postings |
| `eval_pairs.json` | 47 graded candidate–job relevance pairs |
| `fairness_audit_profiles.json` | 10 synthetic counterfactual pairs for offline bias audit |

## Research corpus (`research/`)

Large synthetic eval set for offline benchmarks · see [research/README.md](research/README.md).

| File | Count |
|------|-------|
| `research/cvs.json` | 100 candidates |
| `research/jobs.json` | 50 jobs |
| `research/eval_pairs.json` | 5,000 labeled pairs (relevance 0–3 + rationale) |

Generate: `bash scripts/generate_research_dataset.sh`

## Generated outputs

| Pattern | Source |
|---------|--------|
| `daily_recommendations_YYYY-MM-DD.json` | `POST /match/daily-batch` or legacy agent endpoint |

## Expected regression floats

`data/expected/` · golden metrics for `tests/benchmarks/test_eval_regression.py` (if present).

## Demo linkage

Demo candidate account links to **Rahul Sharma** (`cv_01` in corpus). See [../backend/demo_seed.py](../backend/demo_seed.py).

Do not commit large generated benchmark dumps · see root `.gitignore`.
