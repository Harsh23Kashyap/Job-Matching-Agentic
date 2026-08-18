**Table 6 · Qualitative explanation and fairness examples**

*Label: `tab:qualitative`*

### Example 1: Hallucination

**Case:** Priya Mehta → Frontend Developer

**Context:** Rank 1; explainer=rules

**Explanation:** Matching skills: javascript, react; Role title aligns with your profile (70% title fit); High semantic similarity; Experience aligns with role requirement; Compensation expectations align

**Issue / outcome:** Phantom skill: Java

### Example 2: Low specificity

**Case:** Rahul Sharma → Data Engineer

**Context:** Missing skills: Hadoop|Spark

**Explanation:** Role title differs from your stated background; Moderate semantic similarity; Experience aligns with role requirement; Compensation expectations align; Remote preference may not match role setup

**Issue / outcome:** Explanation omits matched/missing skills; generic component bullets only.

### Example 3: Grounded template (pass)

**Case:** Rahul Sharma → Machine Learning Engineer

**Context:** Faithfulness=1.0, specificity=1.0

**Explanation:** Matching skills: machine learning, python; Role title aligns with your profile (65% title fit); Moderate semantic similarity; Experience aligns with role requirement; Compensation expectations align

**Issue / outcome:** Passes skill mention and component alignment checks.
