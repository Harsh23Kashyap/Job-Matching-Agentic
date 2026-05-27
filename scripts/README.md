# Scripts

Standalone utilities — run from repo root unless noted.

## Files

| Script | Purpose |
|--------|---------|
| `smoke_employer_jobs.py` | Live API smoke for employer jobs flow (backend must be on `:8001`) |
| `run_benchmark.sh` | Lexical vs embedding comparison → `comparison_table.csv` |
| `run_benchmark_eval.sh` | Embedding-only benchmark → `benchmark_*.csv` |

## Usage

```bash
python3 scripts/smoke_employer_jobs.py
bash scripts/run_benchmark.sh
bash scripts/run_benchmark.sh --top-k 10 --prefix exp1
bash scripts/run_benchmark_eval.sh
```

Add new scripts here for one-off smoke, seed, or ops tasks — keep them out of `backend/` package imports when possible.
