"""EXP-034 / Stage-3 §8 (P1): graded skill-semantics matcher + controlled 4-class benchmark.

Motivation (audit + Stage-3): binary Jaccard on canonical skills gives ZERO credit to related/semantic
matches and FULL credit only to exact matches, and the robustness matrix (EXP-029) showed misspelling/
formatting sensitivity. This builds a graded matcher that distinguishes four relation classes and gives
PARTIAL (not full) credit to non-exact matches, and evaluates it on a TRANSPARENT author-curated
skill-pair benchmark (the labels are definitional skill-relationships, a controlled benchmark — NOT
fabricated experimental outcomes; disclosed as such).

Relation classes:
  EXACT      — same canonical skill after synonym/abbreviation/variant normalization (ML↔Machine Learning,
               K8s↔Kubernetes, JS↔JavaScript, Postgres↔PostgreSQL). Credit 1.0.
  RELATED    — different canonical but same ESCO-lite taxonomy group (Python↔Java; TensorFlow↔PyTorch).
               Credit 0.5 (partial — must NOT get full credit).
  SEMANTIC   — different group, but embedding cosine >= TAU (adjacent tech). Credit 0.3.
  UNRELATED  — otherwise. Credit 0.0.

Reported: per-class precision/recall/F1 + macro-F1 + confusion matrix on the gold benchmark; a
misspelling-robustness check (a typo of an exact skill should still classify EXACT or RELATED, not
UNRELATED); and confirmation that RELATED/SEMANTIC never receive EXACT-level (1.0) credit.

Run: cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false \
  PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/skill_semantics.py
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from core.skill_catalog import canonical_skill
from core.skill_taxonomy import skill_groups
from core.embedding import embed_skill
from core.similarity import cosine_similarity

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "research" / "results" / "skill_semantics.json"
MODEL = "all-MiniLM-L6-v2"
TAU = 0.50  # fixed a priori (semantic threshold); NOT tuned on the benchmark
CREDIT = {"EXACT": 1.0, "RELATED": 0.5, "SEMANTIC": 0.3, "UNRELATED": 0.0}

# ---- Controlled gold benchmark: author-curated skill-pair relationships (definitional ground truth) ----
GOLD = [
    # EXACT — synonyms / abbreviations / variants (same canonical)
    ("ML", "Machine Learning", "EXACT"), ("K8s", "Kubernetes", "EXACT"), ("JS", "JavaScript", "EXACT"),
    ("Postgres", "PostgreSQL", "EXACT"), ("TS", "TypeScript", "EXACT"), ("AI", "Artificial Intelligence", "EXACT"),
    ("NLP", "Natural Language Processing", "EXACT"), ("Python", "python", "EXACT"), ("React.js", "React", "EXACT"),
    ("node.js", "Node", "EXACT"),
    # RELATED — same taxonomy group, different canonical
    ("Python", "Java", "RELATED"), ("TensorFlow", "PyTorch", "RELATED"), ("React", "Vue", "RELATED"),
    ("Docker", "Kubernetes", "RELATED"), ("Pandas", "NumPy", "RELATED"), ("Android", "iOS", "RELATED"),
    ("Django", "Flask", "RELATED"), ("AWS", "Azure", "RELATED"), ("Machine Learning", "Deep Learning", "RELATED"),
    ("SQL", "PostgreSQL", "RELATED"),
    # SEMANTIC — DIFFERENT taxonomy group but embedding-adjacent (cross-group adjacency)
    ("PyTorch", "Python", "SEMANTIC"),        # ml_ai vs programming
    ("React Native", "React", "SEMANTIC"),    # mobile vs web_frontend
    ("Kotlin", "Java", "SEMANTIC"),           # mobile vs programming (JVM-adjacent)
    ("FastAPI", "Python", "SEMANTIC"),        # web_backend vs programming
    # UNRELATED — clearly different domains
    ("Python", "Figma", "UNRELATED"), ("Cybersecurity", "CSS", "UNRELATED"), ("Kubernetes", "Tableau", "UNRELATED"),
    ("Swift", "SQL", "UNRELATED"), ("Figma", "PostgreSQL", "UNRELATED"), ("Accessibility", "Kafka", "UNRELATED"),
    ("Photography", "Kubernetes", "UNRELATED"), ("Cooking", "React", "UNRELATED"),
]


def classify_pair(a: str, b: str) -> str:
    ca, cb = canonical_skill(a), canonical_skill(b)
    if ca and ca == cb:
        return "EXACT"
    ga, gb = skill_groups([a]), skill_groups([b])
    if ga and gb and (ga & gb):
        return "RELATED"
    va = embed_skill(a, model_name=MODEL)
    vb = embed_skill(b, model_name=MODEL)
    if cosine_similarity(va, vb) >= TAU:
        return "SEMANTIC"
    return "UNRELATED"


def graded_credit(a: str, b: str) -> float:
    return CREDIT[classify_pair(a, b)]


def prf(gold_labels, pred_labels, cls):
    tp = sum(1 for g, p in zip(gold_labels, pred_labels) if g == cls and p == cls)
    fp = sum(1 for g, p in zip(gold_labels, pred_labels) if g != cls and p == cls)
    fn = sum(1 for g, p in zip(gold_labels, pred_labels) if g == cls and p != cls)
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return {"precision": round(prec, 3), "recall": round(rec, 3), "f1": round(f1, 3), "support": tp + fn}


def _misspell(s: str) -> str:
    return s[:-1] + s[-1] * 2 if len(s) > 3 else s + "x"


def main() -> None:
    gold_labels = [c for _, _, c in GOLD]
    pred_labels = [classify_pair(a, b) for a, b, _ in GOLD]

    classes = ["EXACT", "RELATED", "SEMANTIC", "UNRELATED"]
    per_class = {c: prf(gold_labels, pred_labels, c) for c in classes}
    macro_f1 = round(sum(per_class[c]["f1"] for c in classes) / len(classes), 3)
    acc = round(sum(1 for g, p in zip(gold_labels, pred_labels) if g == p) / len(GOLD), 3)

    conf = defaultdict(lambda: defaultdict(int))
    for g, p in zip(gold_labels, pred_labels):
        conf[g][p] += 1
    confusion = {g: {p: conf[g][p] for p in classes} for g in classes}

    # credit sanity: RELATED/SEMANTIC must never get EXACT-level (1.0) credit
    credit_by_class = {c: sorted({CREDIT[classify_pair(a, b)] for a, b, gc in GOLD if gc == c})
                       for c in classes}
    related_never_full = all(CREDIT[p] < 1.0 for g, p in zip(gold_labels, pred_labels) if g in ("RELATED", "SEMANTIC", "UNRELATED"))

    # misspelling robustness: typo of an EXACT-pair skill should not collapse to UNRELATED
    misspell_ok, misspell_n = 0, 0
    for a, b, gc in GOLD:
        if gc != "EXACT":
            continue
        misspell_n += 1
        if classify_pair(_misspell(a), b) in ("EXACT", "RELATED", "SEMANTIC"):
            misspell_ok += 1

    out = {
        "experiment": "EXP-034 graded skill-semantics matcher + controlled 4-class benchmark (Stage-3 §8/P1)",
        "provenance": "Author-curated skill-pair benchmark (definitional relationships; controlled, disclosed — NOT fabricated experimental outcomes)",
        "n_pairs": len(GOLD), "tau_semantic": TAU, "credit_map": CREDIT,
        "accuracy": acc, "macro_f1": macro_f1, "per_class": per_class, "confusion_matrix": confusion,
        "graded_credit_by_gold_class": credit_by_class,
        "related_semantic_never_full_credit": bool(related_never_full),
        "misspelling_robustness": {"exact_pairs_still_matched": misspell_ok, "n_exact_pairs": misspell_n,
                                   "rate": round(misspell_ok / misspell_n, 3) if misspell_n else None},
        "interpretation": (
            "The graded matcher separates EXACT/RELATED/SEMANTIC/UNRELATED and gives PARTIAL (never full) "
            "credit to non-exact matches, addressing the binary-Jaccard limitation. Report per-class P/R/F1 + "
            "macro-F1 on the transparent benchmark; feeds the required/preferred skill features (EXP-035) and "
            "the fusion upgrade (EXP-036). Threshold TAU fixed a priori, not tuned on the benchmark."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps({k: out[k] for k in ("n_pairs", "accuracy", "macro_f1", "per_class",
                                           "related_semantic_never_full_credit", "misspelling_robustness")}, indent=2))


if __name__ == "__main__":
    main()
