# Core

Business logic: scoring, embeddings, skills, resume/JD text processing, and v2 ML helpers.

## Scoring (product default: composite)

| File | Purpose |
|------|---------|
| `scoring.py` | `compute_semantic`, `compute_multimodal_weighted`, **`compute_composite`** (28/27/10/15/10/10%) |
| `component_scores.py` | Experience, compensation, **title similarity**, remote preference sub-scores |
| `matchmaking_scoring.py` | `score_pair_advanced` · strategy routing, constraints, fusion |
| `skills.py` | Jaccard and soft-embed skill overlap |
| `similarity.py` | Cosine / Euclidean on embedding vectors |
| `rrf.py` | Reciprocal Rank Fusion for ensemble |

## Resume / JD processing

| File | Purpose |
|------|---------|
| `resume_clean.py` | Strip PDF `(cid:N)` artifacts; protect contact spans |
| `contact_extract.py` | Regex: email, phone, GitHub, LinkedIn, portfolio, certs |
| `resume_text.py` | Extract text from PDF/DOCX/TXT uploads |
| `resume_suggestions.py` | Read-only resume coach per job |
| `document_text.py` | Canonical bi-encoder document templates |
| `embedding.py` | `all-MiniLM-L6-v2` lazy singleton |

## Similar entities & explainability

| File | Purpose |
|------|---------|
| `similar_entities.py` | Top-3 similar jobs/candidates by embedding |
| `explain.py` | Rule-based `why_ranked` bullet helpers |

## v2 ML (research / admin)

`lexical.py`, `cross_encoder_rerank.py`, `fusion.py`, `calibration.py`, `constraints.py`, `strategy_router.py`, `feedback_boost.py`, `fairness.py`, `skill_taxonomy.py`
