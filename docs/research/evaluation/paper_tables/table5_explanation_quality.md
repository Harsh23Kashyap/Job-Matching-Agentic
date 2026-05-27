**Explainability evaluation summary (rules vs. grounded template).**

*Label: `tab:explanation-quality`*

| Explainer | Faithfulness | Specificity | Skill mention (%) | No hallucination (%) | Component align (%) | Flagged (%) | Consistency (Jaccard) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Rules | 0.747 | 0.621 | 25.3 | 98.7 | 100.0 | 76.0 | 1.000 |
| Template | 0.962 | 1.000 | 100.0 | 88.7 | 100.0 | 11.3 | 1.000 |

*Note: Automated checks on top-5 composite matches. Faithfulness = pass rate on skill mention, hallucination, and component alignment checks. Consistency = bullet Jaccard on synthetic similar-profile pairs.*
