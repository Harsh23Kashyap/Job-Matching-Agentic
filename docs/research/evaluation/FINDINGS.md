# Research Findings — Synthesis

Run ID: `2026-05-27T150000Z`

## Corpus

- 30 candidate profiles, 15 job postings, 30 labeled queries (47 graded pairs)
- Graded relevance 0–2 in `data/eval_pairs.json`; binary relevant = grade > 0
- Evaluation protocol: exhaustive ranking (all jobs scored per query)

## Headline results (K=5)

1. **Best embedding strategy:** Multimodal weighted blend — nDCG@5=0.924, MRR=0.961
2. **Production composite (ablation):** nDCG@5=0.942, R@5=0.983 — best among ablation variants
3. **Significant vs semantic baseline (nDCG, p<0.05):** Multimodal weighted blend, RRF ensemble
4. **Cross-encoder on composite:** nDCG Δ=-0.108 (quality ↓, latency ↑ ~141 ms/query)

## Limitations

- Small fixed corpus (n=30 queries) — bootstrap CIs are wide
- Exhaustive evaluation ≠ ANN production path (see phase11 for store sweep)
- Cross-encoder model adds heavy latency; not default in portals
- Composite weights (40/30/15/10/5) are hand-tuned, not learned

## Artifact index

See `artifacts/manifest.json` and per-study folders under `artifacts/runs/<run_id>/`.
