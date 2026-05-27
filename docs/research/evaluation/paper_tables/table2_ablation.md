**Ablation over composite matching components (K=5).**

*Label: `tab:ablation`*

| Variant | Category | P@5 | R@5 | MRR | nDCG@5 | MAP |
| --- | --- | --- | --- | --- | --- | --- |
| Full composite | Full | 0.307 | 0.983 | 0.944 | **0.942** | 0.896 |
| Semantic + skills | Partial | 0.287 | 0.933 | 0.961 | 0.917 | 0.867 |
| Semantic + skills + experience | Partial | 0.287 | 0.933 | 0.961 | 0.917 | 0.866 |
| Semantic only | Single | 0.267 | 0.867 | 0.931 | 0.878 | 0.810 |
| Skills only | Single | 0.233 | 0.733 | 0.816 | 0.748 | 0.681 |
| RRF ensemble | Ensemble | 0.233 | 0.717 | 0.570 | 0.564 | 0.497 |
| Compensation only | Single | 0.187 | 0.567 | 0.457 | 0.393 | 0.387 |
| Location only | Single | 0.167 | 0.467 | 0.388 | 0.335 | 0.328 |
| Experience only | Single | 0.160 | 0.467 | 0.384 | 0.326 | 0.314 |

*Note: Composite weights: semantic 40%, skills 30%, experience 15%, compensation 10%, location 5%. Partial variants use renormalized weights.*
