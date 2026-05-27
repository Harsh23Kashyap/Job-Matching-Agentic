# Synthetic Research Corpus

Large-scale **synthetic** evaluation dataset for offline benchmark research.  
Not used by production bootstrap · the demo corpus remains `data/cvs.json` + `data/jobs.json`.

## Contents

| File | Description |
|------|-------------|
| `cvs.json` | 100 candidate profiles (`rcv_001` … `rcv_100`) |
| `jobs.json` | 50 job postings (`rjob_001` … `rjob_050`) |
| `eval_pairs.json` | 5,000 labeled pairs (full 100×50 matrix) with relevance 0–3 + rationale |
| `manifest.json` | Generation metadata, role counts, relevance distribution |

## Role families (8)

`backend`, `frontend`, `ml`, `data`, `devops`, `mobile`, `product`, `design`

Each candidate and job carries a `role` field. Skills are sampled from role-specific pools.

## Relevance scale (0–3)

| Grade | Meaning |
|-------|---------|
| **3** | Strong match · same role, ≥75% required skill overlap, experience met |
| **2** | Good match · same role with moderate overlap, or adjacent role with overlap |
| **1** | Partial · minimal overlap or adjacent role |
| **0** | Not relevant · different role, negligible overlap |

Each label includes an auto-generated **rationale** citing role alignment, skill overlap, experience, remote, and salary fit.

## Regenerate

```bash
bash scripts/generate_research_dataset.sh
# or:
cd backend && python -m benchmarks.run_generate_research_dataset

# Custom size / seed:
python -m benchmarks.run_generate_research_dataset --candidates 100 --jobs 50 --seed 42

# Sparse labels (~15 jobs per candidate instead of full matrix):
python -m benchmarks.run_generate_research_dataset --sparse-labels
```

## Use in benchmarks

```bash
python -m benchmarks.run_eval \
  --data-dir ../data/research \
  --eval-path ../data/research/eval_pairs.json
```

## Labeling logic

Implemented in `backend/benchmarks/synthetic_dataset/roles.py`:

- Skill overlap (Jaccard on normalized required skills)
- Role same / adjacent / different graph
- Experience gap, remote preference, salary vs budget

Deterministic for a given `--seed`.
