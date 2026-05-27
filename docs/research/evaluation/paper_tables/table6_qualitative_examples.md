**Table 6 · Qualitative explanation and fairness examples**

*Label: `tab:qualitative`*

### Example 1: Hallucination

**Case:** Priya Mehta → Frontend Developer

**Context:** Rank 1; explainer=rules

**Explanation:** Matching skills: javascript, react; Title/summary overlap: developer, frontend; High semantic similarity; Experience aligns with role requirement

**Issue / outcome:** Phantom skill: Java

### Example 2: Low specificity

**Case:** Rahul Sharma → Data Engineer

**Context:** Missing skills: Spark|Hadoop

**Explanation:** Moderate semantic similarity; Experience aligns with role requirement; Compensation expectations align; Composite score blends semantic, skills, experience, compensation, and location signals

**Issue / outcome:** Explanation omits matched/missing skills; generic component bullets only.

### Example 3: Fairness (rank shift)

**Case:** Synthetic pair `nationality_phrase_01`

**Context:** Field changed: summary_suffix; max score Δ=0.0087

**Explanation:** Ranking order changed for top-1 job when only demographic-like metadata differed.

**Issue / outcome:** explanation_drift|rank_change_in_top_k_union|top_1_changed

### Example 4: Grounded template (pass)

**Case:** Rahul Sharma → Machine Learning Engineer

**Context:** Faithfulness=1.0, specificity=1.0

**Explanation:** Matching skills: machine learning, python; Title/summary overlap: engineer, learning, machine; High semantic similarity; Experience aligns with role requirement; Gaps: TensorFlow

**Issue / outcome:** Passes skill mention and component alignment checks.
