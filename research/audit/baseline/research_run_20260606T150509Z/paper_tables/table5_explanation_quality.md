**Explainability evaluation summary (rules vs. grounded template).**

*Label: `tab:explanation-quality`*

| Explainer | Faithfulness | Specificity | Skill mention (%) | No hallucination (%) | Component align (%) | Flagged (%) | Consistency (Jaccard) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Rules | 0.745 | 0.627 | 25.3 | 98.0 | 100.0 | 76.7 | 1.000 |
| Template | 0.747 | 0.633 | 26.7 | 97.3 | 100.0 | 76.0 | 1.000 |

*Note: Automated checks on top-5 composite matches. Faithfulness = pass rate on skill mention, hallucination, and component alignment checks. Consistency = bullet Jaccard on synthetic similar-profile pairs.*
