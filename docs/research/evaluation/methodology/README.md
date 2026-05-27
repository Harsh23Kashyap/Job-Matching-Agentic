# Methodology

Fixed documentation for the evaluation protocol. These files are **not** auto-regenerated — update manually if the protocol changes.

| Doc | Contents |
|-----|----------|
| [corpus-and-labels.md](corpus-and-labels.md) | 30 CV / 15 job corpus, eval_pairs format, relevance grades |
| [metrics-and-protocols.md](metrics-and-protocols.md) | P@K, R@K, MRR, nDCG, MAP; exhaustive vs ANN vs CE |
| [statistical-testing.md](statistical-testing.md) | Paired bootstrap (5000 resamples), p-values, W/L/T |
| [fairness-audit.md](fairness-audit.md) | Synthetic counterfactual bias audit (offline only) |
| [explainability-evaluation.md](explainability-evaluation.md) | Match explanation faithfulness & hallucination checks |

Auto-generated results live in [../studies/](../studies/) and [../artifacts/](../artifacts/).
