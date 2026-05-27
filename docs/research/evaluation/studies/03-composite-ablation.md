# Study 3 · Composite Matching Ablation

## Production composite weights

| Component | Weight |
|-----------|--------|
| Semantic | 40% |
| Skills | 30% |
| Experience | 15% |
| Compensation | 10% |
| Location | 5% |

- **Skills mode:** jaccard
- **Best variant (nDCG):** Full composite

## Variants

| Variant | Category | Components | P@K | R@K | MRR | nDCG@K | MAP | ms |
|---------|----------|------------|-----|-----|-----|--------|-----|-----|
| Semantic only | single | semantic | 0.267 | 0.867 | 0.931 | 0.878 | 0.810 | 0.22 |
| Skills only | single | skills | 0.233 | 0.733 | 0.816 | 0.748 | 0.681 | 0.04 |
| Experience only | single | experience | 0.160 | 0.467 | 0.384 | 0.326 | 0.314 | 0.02 |
| Compensation only | single | compensation | 0.187 | 0.567 | 0.457 | 0.393 | 0.387 | 0.02 |
| Location only | single | location | 0.167 | 0.467 | 0.388 | 0.335 | 0.328 | 0.02 |
| Semantic + skills | partial | semantic+skills | 0.287 | 0.933 | 0.961 | 0.917 | 0.867 | 0.28 |
| Semantic + skills + experience | partial | semantic+skills+experience | 0.287 | 0.933 | 0.961 | 0.917 | 0.866 | 0.27 |
| Full composite | full | semantic+skills+experience+compensation+location | 0.307 | 0.983 | 0.944 | 0.942 | 0.896 | 0.26 |
| RRF ensemble | ensemble | RRF(semantic,skills,experience,compensation,location) | 0.233 | 0.717 | 0.570 | 0.564 | 0.497 | 0.32 |

## Findings

- Semantic-only is the strongest single signal (nDCG ~0.88).
- Structural signals alone (experience, compensation, location) rank poorly in isolation.
- Full weighted composite (40/30/15/10/5) achieves best nDCG on this corpus.
- RRF over single-component rankers underperforms weighted composite here.
