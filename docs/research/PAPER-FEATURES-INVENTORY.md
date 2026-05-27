# Implementation Features Inventory — Research Paper Context

**Project:** Job-Matching-Agentic  
**Last updated:** 2026-05-27  
**Purpose:** Single reference for manuscript writing — what is built, how it works, what is deferred, and what to claim vs. not claim.

**Related docs:** [HLD](../design/HLD-multi-agent-system.md) · [SDD](../design/SDD-multi-agent-system.md) · [V1-V2 scope](../design/V1-V2-SCOPE.md) · [V1.1 portals spec](../design/v1.1-role-portals-auth.md)

---

## 1. Executive summary (for paper abstract / contributions)

We implemented a **three-agent job matching system** with:

- **Candidate Agent** — resume/CV ingest, validation, embedding, vector storage, profile state
- **Employer Agent** — job description ingest, validation, embedding, vector storage, job state
- **Matchmaking Agent** — read-only scoring, ranking, explanation; never writes to vector stores

Communication uses an **in-process event-driven bus** (event-driven monolith, not microservices). Matching combines **semantic bi-encoder similarity** (MiniLM-L6-v2, 384-d) with **skill overlap** (Jaccard or soft embedding), optional **RRF ensemble** over multiple strategy×metric lists, and **rule-based transparency** (`why_ranked` bullets).

**V1.1 extension:** role-based web portals (Candidate / Employer / Admin), session authentication, and **LLM-assisted resume parsing** (Ollama or OpenAI-compatible) with human-in-the-loop profile review.

**Evaluation corpus:** 30 synthetic CVs, 15 jobs, 47 labeled relevance pairs (0–2 scale). Smoke validation: *Rahul Sharma → Machine Learning Engineer* rank 1.

**Test suite:** 59 automated tests (unit + integration).

---

## 2. System architecture (claim in §3 / methodology)

### 2.1 Pattern

| Aspect | Implementation |
|--------|----------------|
| Architecture style | Event-driven monolith |
| Agents | 3 Python classes with explicit state ownership |
| Communication | `AgentEventBus` — synchronous pub-sub, in-process |
| API layer | Thin FastAPI gateway; agents accessed via `app.state.container` |
| Persistence | Chroma (vectors) + SQLite (users/ownership, v1.1) |
| Frontend | React 19 + Vite + React Router (v1.1 portals) |

### 2.2 Agent responsibilities

| Agent | Owns | Does NOT do |
|-------|------|-------------|
| **Candidate Agent** | `candidates_collection`, profile dict, name index, CV register/bootstrap | Match scoring |
| **Employer Agent** | `jobs_collection`, job dict, title index, JD register/bootstrap | Match scoring |
| **Matchmaking Agent** | Match sessions (≤50), score/rank/explain | Write to Chroma; mutate profiles |

### 2.3 Event types (observable agent coordination)

| Event | Publisher | Meaning |
|-------|-----------|---------|
| `candidate.profile.updated` | Candidate Agent | Profile registered or updated |
| `job.profile.updated` | Employer Agent | Job registered or updated |
| `system.corpus.bootstrapped` | System | Startup load of JSON corpus complete |
| `match.requested` | Matchmaking Agent | Match run initiated |
| `match.completed` | Matchmaking Agent | Ranked results ready |

### 2.4 Design principles (ethics / Khan guardrails)

- **Human-in-the-loop:** UI presents ranks; no automated hiring decision
- **Transparency:** Per-result `why_ranked`, agent status panel, OpenAPI docs
- **Bias monitoring:** Acknowledged in design docs; no automated fairness metrics in v1/v1.1
- **Naming:** **Candidate Agent** (not Client/Employee split) — consistent code, UI, paper

---

## 3. Multi-agent workflows (implemented)

| Workflow | Direction | Retrieval mode | Status |
|----------|-----------|----------------|--------|
| Single-strategy match | Candidate → jobs | Exhaustive over full corpus | ✅ |
| Single-strategy match | Job → candidates | Exhaustive over full corpus | ✅ |
| RRF ensemble | Either | Multiple ranked lists fused (k=60) | ✅ |
| Daily batch recommendations | All candidates → top jobs | ANN shortlist per candidate | ✅ |
| Corpus bootstrap | JSON files → agents + Chroma | On startup | ✅ |
| Register new CV | POST `/candidates` | Immediate embed + upsert | ✅ |
| Register new JD | POST `/jobs` | Immediate embed + upsert | ✅ |
| Resume upload + LLM extract | Candidate portal | PDF/DOCX/TXT → structured fields | ✅ v1.1 |
| Real external job API sync | — | — | ❌ v2 |
| Agent event log API | — | — | ❌ v2 |

---

## 4. Machine learning & matching (implemented)

### 4.1 Representation

| Component | Detail |
|-----------|--------|
| Bi-encoder | `sentence-transformers/all-MiniLM-L6-v2` |
| Embedding dim | 384 |
| Document construction | Normative field order in `core/document_text.py` (benchmark-safe templates) |
| Skill normalization | Alias catalog before overlap (`core/skills.py`) |

### 4.2 Matching strategies

| Strategy | Formula / behavior | Configurable |
|----------|-------------------|--------------|
| **Semantic** | Cosine or Euclidean-derived similarity on document embeddings | `metric`: cosine, euclidean |
| **Multimodal** | `α × semantic + (1−α) × skills` with default α=0.7 | `semantic_weight`, `skills_mode` |
| **Skills — Jaccard** | Set overlap on normalized skill strings | `skills_mode=jaccard` |
| **Skills — soft embed** | Embedding similarity on skill sets | `skills_mode=soft_embed` |

### 4.3 Fusion & retrieval

| Feature | Detail |
|---------|--------|
| **RRF ensemble** | Reciprocal Rank Fusion, k=60; combines multiple strategy×metric ranked lists |
| **UI match retrieval** | Exhaustive — scores all jobs (≤15) or all candidates (≤30) |
| **Daily batch retrieval** | ANN via Chroma `search_jobs` with candidate pool limit |
| **Default strategy** | Semantic cosine (user can toggle multimodal, metric, skills mode) |

### 4.4 Explanations

| Feature | Detail |
|---------|--------|
| Explainer | `RuleExplainer` — deterministic, no LLM |
| `why_ranked` bullets | Skill overlap, title/summary token overlap, semantic tier, multimodal breakdown |
| Max reasons | 4 per ranked result |

### 4.5 Parsers

| Parser | Input | Output | Status |
|--------|-------|--------|--------|
| `JsonParser` | Structured JSON dict | `CandidateProfile` / `JobProfile` | ✅ v1 |
| `LlmParser` | Unstructured resume text | Structured candidate fields (JSON) | ✅ v1.1 |
| LLM JD parser | Unstructured JD prose | `JobProfile` | ❌ v2 |
| LLM match explainer | Scores + profiles | Natural language | ❌ v2 |

### 4.6 Deferred ML (do NOT claim as implemented)

- BM25 / TF-IDF lexical baselines
- Cross-encoder rerank (ms-marco two-stage)
- Bootstrap significance testing (paired nDCG CI)
- Full Table 9 progression ladder / phase11 ANN sweep
- BGE-small embedder ablation
- LLM rerank / LLM strategy selection
- Preference learning from clicks

---

## 5. Data model

### 5.1 Candidate profile fields

`id`, `name`, `skills[]`, `experience_years`, `preferred_salary`, `remote_preference`, `summary`, `version`, `document_text`, `document_text_hash`, `embedding`

### 5.2 Job profile fields

`id`, `title`, `required_skills[]`, `required_experience`, `budget`, `remote_policy`, `description`, `company`, `location`, `job_type`, `link`, `version`, `document_text`, `document_text_hash`, `embedding`

### 5.3 Evaluation corpus

| Asset | Count | Source |
|-------|-------|--------|
| CVs (`data/cvs.json`) | 30 | Legacy Agentic-Job-Matching repo |
| Jobs (`data/jobs.json`) | 15 | Legacy repo |
| Labeled pairs (`data/eval_pairs.json`) | 47 | relevance 0–2 scale |
| Daily batch output | Dated JSON under `data/daily_recommendations_YYYY-MM-DD.json` | Generated at runtime |

### 5.4 Key smoke test (reproducible claim)

**Query:** Rahul Sharma (candidate)  
**Expected top job:** Machine Learning Engineer (rank 1)  
**Strategy:** semantic cosine (default)

---

## 6. Vector store & infrastructure

| Item | v1 / v1.1 | v2 |
|------|-----------|-----|
| Vector DB | Chroma persistent (`backend/chroma_db/`) | Qdrant switch planned |
| Collections | `candidates_collection`, `jobs_collection` | — |
| User DB | SQLite (`backend/app.db`) — users, ownership | Postgres for production |
| Event bus | In-process | Redis/NATS for microservices |
| Auth | HTTP-only session cookie, bcrypt | OAuth, email verify |

---

## 7. API surface (complete list)

### 7.1 Authentication (v1.1)

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/auth/register` | Email, password, role (candidate/employer/admin) |
| POST | `/auth/login` | Session cookie |
| POST | `/auth/logout` | Clear session |
| GET | `/auth/me` | Current user |

### 7.2 Agents & system

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/agents/status` | Counts, store version, last event per agent |
| GET | `/system/config` | Strategies, metrics, skills modes, store label |

### 7.3 Candidates

| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| GET | `/candidates` | Public | List names |
| GET | `/candidates/full` | Public | Full profiles (no embedding) |
| GET | `/candidates/{name}` | Public | Single profile |
| GET | `/candidates/me` | Candidate | Owned profile |
| POST | `/candidates/upload-resume` | Candidate | Multipart PDF/DOCX/TXT → LLM extract |
| POST | `/candidates` | Optional | Register/update profile; links ownership if candidate session |

### 7.4 Jobs

| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| GET | `/jobs` | Public | List titles |
| GET | `/jobs/full` | Public | Full profiles |
| GET | `/jobs/{title}` | Public | Single job |
| GET | `/jobs/mine` | Employer | Owned jobs |
| POST | `/jobs` | Optional | Register job; links ownership if employer session |

### 7.5 Matching

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/match/candidate-to-jobs` | Single-strategy CV→jobs |
| POST | `/match/job-to-candidates` | Single-strategy JD→candidates |
| POST | `/match/ensemble` | RRF over configured search list |
| POST | `/match/daily-batch` | ANN batch → dated JSON artifact |

### 7.6 Legacy aliases (backward compatibility)

`/match-resume`, `/match-job`, `/match-resume-ensemble`, `/agent/run-daily-recommendations`

---

## 8. Frontend features

### 8.1 Stack

React 19, Vite 6/7, axios, react-router-dom v7, light/dark theme (localStorage)

### 8.2 Role portals (v1.1)

| Portal | Routes | Features |
|--------|--------|----------|
| **Public** | `/login`, `/register` | Role picker at signup (candidate / employer / admin) |
| **Candidate** | `/candidate/onboarding`, `/profile`, `/matches` | Resume upload → LLM extract → edit → save → find jobs |
| **Employer** | `/employer/jobs`, `/matches` | Create/list owned jobs → find ranked candidates |
| **Admin** | `/admin/console` | Full eval Match Console (unchanged from v1) |

### 8.3 Admin Match Console components

| Component | Capability |
|-----------|------------|
| `AgentStatusPanel` | Live KPI cards: 3 agents, entity counts, last event, API health |
| `MatchControls` | Mode toggle (CV→jobs / JD→candidates), entity picker, strategy, metric, skills mode, ensemble, top-K, daily batch |
| `ResultsPanel` | Ranked table, score breakdown, `why_ranked`, error states, recent runs sidebar |
| Theme toggle | Light-first professional UI; frosted header |

### 8.4 Candidate / employer UX (simplified vs admin)

- No agent status panel, ensemble knobs, or daily batch
- Single-click match with default semantic cosine + Jaccard skills
- Profile required before candidate job search

### 8.5 Client persistence

- `jm_recent_runs` — last 10 match results (admin console)
- `jm_theme` — light/dark preference

---

## 9. LLM resume pipeline (v1.1 — hybrid agentic)

```
Upload (PDF/DOCX/TXT, max 5MB)
  → text extraction (pdfplumber / DOCX XML)
  → LlmParser.parse_candidate_from_text()
      → Ollama /api/chat (format: json) OR OpenAI-compatible API
      → Pydantic-normalized fields
  → user review/edit form
  → POST /candidates → CandidateAgent.register → Chroma upsert
  → POST /match/candidate-to-jobs
```

**Fallback:** If LLM unavailable (503), user fills form manually.  
**Human-in-the-loop:** Extraction is assistive; user must review before save.

---

## 10. Testing & validation

### 10.1 Test inventory (59 total)

| Area | File(s) | Tests |
|------|---------|-------|
| Scoring / ML core | `test_scoring.py`, `test_rrf.py` | 10 |
| Parser / snapshots | `test_parser.py`, `test_snapshots.py` | 4 |
| Event bus | `test_event_bus.py` | 4 |
| Chroma store | `test_chroma_store.py` | 2 |
| Agents | `test_candidate_agent.py`, `test_employer_agent.py`, `test_matchmaking_agent.py` | 6 |
| Bootstrap / match flow | `test_bootstrap.py`, `test_match_flow.py`, `test_daily_batch.py` | 7 |
| API gateway | `test_api_gateway.py` | 8 |
| Auth | `test_auth_api.py` | 8 |
| LLM / resume | `test_llm_parser.py`, `test_resume_text.py`, `test_resume_upload.py` | 10 |

### 10.2 What we validate today

- Corpus bootstrap: 30 candidates, 15 jobs
- End-to-end match: Rahul Sharma → ML Engineer rank 1
- RRF fusion correctness (unit)
- Auth session lifecycle
- Resume upload with mocked LLM

### 10.3 What we do NOT validate yet (v2)

- Full Table 9/10 benchmark reproduction
- Bootstrap statistical significance
- Cross-encoder nDCG 0.939 row
- 63-test legacy parity
- Fairness / demographic bias metrics

---

## 11. Documentation artifacts (for paper cross-reference)

| Document | Path | Use in paper |
|----------|------|--------------|
| High-Level Design | `docs/design/HLD-multi-agent-system.md` | §3 architecture narrative |
| Software Design Document | `docs/design/SDD-multi-agent-system.md` | Implementation detail, API contracts |
| V1 vs V2 scope | `docs/design/V1-V2-SCOPE.md` | Limitations / future work |
| V1.1 portals | `docs/design/v1.1-role-portals-auth.md` | Product UX + auth + LLM CV |
| Knowledge graph | `.claude/knowledge_graph.md` | Legacy paper↔code traceability |
| Brainstorm decisions | `.claude/brainstorm-history.md` | Design decision audit trail |
| This inventory | `docs/research/PAPER-FEATURES-INVENTORY.md` | Master feature checklist |

---

## 12. Suggested paper section mapping

| Paper section | Source material |
|---------------|-----------------|
| **§1 Introduction / motivation** | Khan Part VIII framing (knowledge graph §2b); human-in-the-loop hiring |
| **§3 System architecture** | HLD §2–4; three-agent diagram; event bus; data ownership |
| **§4 Matching methodology** | Semantic + multimodal formulas; skills modes; RRF; document templates |
| **§5 Evaluation** | 30/15/47 corpus; smoke test; defer full Table 9 to v2 or "preliminary" |
| **§6 Application / demo** | Admin console + role portals; agent status panel; `why_ranked` |
| **§7 Hybrid agentic layer** | JsonParser (structured) + LlmParser (unstructured CV); v2 LLM explainer deferred |
| **§8 Ethics** | No auto-hire; transparency; bias acknowledged not measured |
| **§9 Future work** | V2 scope: lexical, CE rerank, fairness, scale, LLM JD/explainer |

---

## 13. Contribution bullets (draft — edit for venue)

1. **Three-agent architecture** for job matching with explicit state ownership and event-driven coordination in a deployable monolith.
2. **Configurable multi-signal matching** — semantic bi-encoder, Jaccard/soft skill overlap, multimodal blend, and RRF ensemble — exposed via API and admin UI.
3. **Transparent ranking** — rule-based `why_ranked` explanations alongside numeric score breakdowns.
4. **Hybrid structured + LLM parsing** — deterministic JSON pipeline for eval corpus; LLM-assisted resume onboarding with mandatory human review (v1.1).
5. **Role-based demonstration platform** — separate candidate, employer, and admin experiences with session auth, preserving research eval console.
6. **Reproducible evaluation harness** — 30 CV / 15 job corpus with 47 labeled pairs and automated smoke + 59-test suite.

---

## 14. Explicit non-claims (reviewer safety)

Do **not** state as implemented unless v2 is done:

- Cross-encoder reranking or LLM rerank
- BM25/TF-IDF lexical retrieval
- Statistical significance / bootstrap CIs on nDCG
- Qdrant vs Chroma latency study
- OAuth / production-grade auth
- Automated fairness or bias evaluation
- ESCO/O*NET skill taxonomy
- Real-time external job board ingestion
- Autonomous LLM agent strategy selection

---

## 15. Tech stack summary (for implementation footnote)

| Layer | Technologies |
|-------|--------------|
| Backend | Python 3.11, FastAPI 0.129, uvicorn, pydantic v2 |
| ML | sentence-transformers, numpy, Chroma 0.4 |
| Auth | passlib/bcrypt, Starlette SessionMiddleware, SQLite |
| LLM | httpx → Ollama or OpenAI-compatible API; pdfplumber |
| Frontend | React 19, Vite, axios, react-router-dom |
| Tests | pytest 8.3, FastAPI TestClient, httpx mocks |

---

## 16. Version timeline

| Release | Date | Highlights |
|---------|------|------------|
| **V1** | 2026-05-27 | Three agents, core ML, Chroma, admin Match Console, 41 tests |
| **V1.1** | 2026-05-27 | Auth, 3 portals, LLM resume upload, ownership APIs, 59 tests |
| **V2** | Planned | Benchmarks, CE rerank, LLM JD/explainer, Qdrant, fairness |
