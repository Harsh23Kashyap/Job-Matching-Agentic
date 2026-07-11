# V1 vs V2 Implementation Scope

**Project:** Job-Matching-Agentic (multi-agent rewrite)  
**Date:** 2026-05-27  
**Status:** Approved scope for implementation planning  
**Related:** [HLD](./HLD-multi-agent-system.md) · [SDD](./SDD-multi-agent-system.md)

---

## Summary

| | V1 | V2 |
|---|----|----|
| **Goal** | Working three-agent demo + full UI + core ML matching | Benchmark parity, advanced ML stages, LLM layer, scale |
| **Architecture** | Event-driven monolith, 3 agents + thin API gateway | Optional service split, Redis bus, Qdrant, real jobs |
| **Paper** | Code first; manuscript updated after demo works | Full §2 lit review, LLM claims, taxonomy, fairness eval |
| **Est. effort** | ~7–8 dev days (per SDD) | TBD after v1 demo |

---

## V1 · Ship in first release

### Architecture & agents

| Item | Detail |
|------|--------|
| **Candidate Agent** | Owns CV ingest, validation, skill catalog, embed, Chroma `candidates_collection`, profile state, events |
| **Employer Agent** | Owns JD ingest, validation, embed, Chroma `jobs_collection`, job state, events |
| **Matchmaking Agent** | Reads snapshots from both agents; scores, ranks, explains; never writes to vector stores |
| **Event bus** | In-process pub-sub (`AgentEventBus`); sync handlers |
| **Events** | `CandidateProfileUpdated`, `JobProfileUpdated`, `CorpusBootstrapped`, `MatchCompleted` |
| **Bootstrap** | Load `data/cvs.json` + `data/jobs.json` from legacy repo copy on startup |
| **Naming** | **Candidate Agent** (code, paper, UI · no Client/Employee split) |

### Core ML / matching (v1)

| Item | Detail |
|------|--------|
| **Bi-encoder** | `all-MiniLM-L6-v2`, 384-d, sentence-transformers |
| **Document templates** | Normative field order (`core/document_text.py`) · benchmark-safe |
| **Skill catalog** | Alias normalization before overlap |
| **Semantic strategy** | Cosine + Euclidean-derived similarity |
| **Multimodal strategy** | Weighted blend @ α=0.7 |
| **Skills modes** | **Jaccard** and **soft skill embed** · exposed in API + UI |
| **Default strategy** | **Semantic cosine** (user toggles multimodal) |
| **RRF ensemble** | k=60; multiple strategy×metric lists |
| **Retrieval · UI match** | **Exhaustive** over full corpus (≤15 jobs) |
| **Retrieval · daily batch** | **ANN** shortlist via agent `search_jobs` |
| **Explanations** | Rule-based `why_ranked` bullets (`RuleExplainer`) |
| **Parser** | `JsonParser` · Pydantic validation only |

### Vector store (v1)

| Item | Detail |
|------|--------|
| **Backend** | **Chroma only** (persistent `backend/chroma_db/`) |
| **Collections** | `candidates_collection`, `jobs_collection` |
| **Qdrant** | Not in v1 UI or default config |

### API gateway

| Item | Detail |
|------|--------|
| **New routes** | `/candidates`, `/jobs`, `/match/candidate-to-jobs`, `/match/job-to-candidates`, `/match/ensemble`, `/match/daily-batch`, `/agents/status`, `/system/config` |
| **Legacy aliases** | `/match-resume`, `/match-job`, `/match-resume-ensemble`, `/match-job-ensemble`, `/agent/run-daily-recommendations` → map to new handlers |
| **Agent observability** | `GET /agents/status` · entity counts, store version, last event |
| **Skills mode param** | On match + ensemble requests |
| **Auth** | None (local research demo) |

### V1.1 · Role portals, auth, LLM resume (shipped)

| Item | Detail |
|------|--------|
| **Auth** | Email/password, HTTP-only session cookie, SQLite user store |
| **Portals** | Candidate, Employer, Admin · React Router role-guarded routes |
| **LLM CV parser** | `LlmParser` · Ollama default; OpenAI-compatible fallback |
| **Resume upload** | `POST /candidates/upload-resume` (PDF/DOCX/TXT) |
| **Ownership** | `GET /candidates/me`, `GET /jobs/mine`; 1:1 candidate profile per user |
| **Tests** | 59 total (41 v1 + 18 v1.1) |

### Agent workflows (v1)

| Workflow | In v1? |
|----------|--------|
| Candidate → jobs match | yes |
| Job → candidates match | yes |
| RRF ensemble (4 strategy×metric combos) | yes |
| Daily batch recommendations + dated JSON | yes |
| Register new CV/JD via POST | yes |
| Real jobs external API sync | no → v2 |
| Agent event log API (`/agents/events/recent`) | no → v2 (optional v1.1) |

### Frontend (v1 · full rewrite)

| Item | Detail |
|------|--------|
| **Stack** | React 19 + Vite 7 + axios |
| **AgentStatusPanel** | Three agent cards (count, version, last event) |
| **MatchControls** | Mode toggle, entity select, strategy, metric, **skills mode**, ensemble, top-K |
| **ResultsPanel** | Ranked cards, score breakdown, why_ranked |
| **Ops** | Daily batch trigger, vector store display (Chroma label) |
| **Persistence** | localStorage for saved configs + recent runs + theme |

### Data & eval (v1)

| Item | Detail |
|------|--------|
| **Corpus copy** | `data/cvs.json`, `data/jobs.json`, `data/eval_pairs.json` from legacy `Agentic-Job-Matching` repo |
| **Smoke test** | End-to-end: Rahul Sharma → Machine Learning Engineer rank 1 |
| **Unit + integration tests** | Agent contracts, event bus, bootstrap, API gateway (target ≥40 tests) |
| **Benchmark regression gate** | **Deferred** · no hard block on Table 9/10 floats in v1 |

### Documentation (v1)

| Item | Detail |
|------|--------|
| HLD / SDD / this scope doc | yes |
| README · run instructions | yes |
| Paper intro + §3 diagram | After working demo (code first) |

### Ethics / Khan guardrails (v1)

| Item | Detail |
|------|--------|
| Human-in-the-loop | UI presents ranks; no auto-hire |
| Transparency | `why_ranked`, agent status panel, OpenAPI docs |
| Bias monitoring | Acknowledged in docs; no automated fairness metrics yet |

---

## V2 · Parked for later

### Advanced ML & benchmarks

| Item | Why v2 |
|------|--------|
| **BM25 + TF-IDF lexical baselines** | Table 9 rows 0–1; needs `core/lexical.py` + tiktoken |
| **Cross-encoder rerank** | Two-stage pool=10, ms-marco, blend 0.4/0.6 · progression row 6 |
| **Bootstrap significance** | Paired nDCG CI, 5000 resamples · `paper_bootstrap_significance.json` |
| **Full `paper_progression` driver** | Complete Table 9 ladder as merge gate |
| **Full `phase11` driver** | 40-config ANN sweep + latency table |
| **Rich templates ablation** | `BENCHMARK_RICH_TEMPLATES=1` |
| **BGE-small embedder ablation** | Alternate `EMBEDDING_MODEL` row |
| **RRF list alignment** | Resolve paper §4 vs `paper_progression` four-list mismatch |

### LLM / hybrid agentic layer

| Item | Why v2 |
|------|--------|
| **LLM JD parser** | Unstructured prose → `JobProfile` |
| **LLM match explainer** | Natural-language why_ranked |
| **LLM query refinement** | Interpret user intent |
| **LLM strategy selection** | Agent picks strategy (§9.1 future work) |
| **LLM rerank** | Ollama/Mistral blend · was in old paper, never built |
| **AI-use disclosure policy** | Applicant + employer rules for assisted documents |

### Infrastructure & scale

| Item | Why v2 |
|------|--------|
| **Qdrant vector store** | Switch in UI + phase11 parity (~2× latency story) |
| **Redis / NATS event bus** | Extract agents to microservices |
| **Real jobs sync** | `real_jobs_sync.py` → Employer Agent external API |
| **ANN-first UI matching** | Scale beyond 15-job corpus (§9.3) |
| **Read-only demo mode** | `settings.read_only` disable POST |
| **Authentication (production)** | OAuth, email verification, Postgres, public deploy hardening · basic auth shipped in v1.1 |

### Frontend & ops (v2)

| Item | Why v2 |
|------|--------|
| **Agent event log panel** | `GET /agents/events/recent` |
| **Per-search ensemble weights** | Currently hardcoded 1.0 |
| **Semantic weight slider** | Advanced UI; v1 fixed 0.7 via API |
| **Preference / click feedback** | §9.2 embedding from interactions |

### Paper & research (v2)

| Item | Why v2 |
|------|--------|
| **Literature review rewrite** | Recruitment systems, AI agents in hiring, gaps |
| **Full white-paper intro** | Khan Part VIII narrative, no §1.x subsections |
| **New §3 multi-agent block diagram** | After code matches diagram |
| **§5 Quality Metrics** | Full DCG/IDCG formulas, bootstrap prose |
| **Portal PDF sync** | Cover letter + information sheet metrics |
| **ESCO/O*NET skill taxonomy** | §9.5 · replace string skills |
| **Fairness evaluation** | Demographic proxy testing on larger corpus |
| **Larger labeled dataset** | Beyond 30/15/47 synthetic pairs |

### Legacy parity checklist (v2 target)

Reproduce from old `Agentic-Job-Matching` repo:

- [ ] Table 9 all 8 progression rows (exact floats)
- [ ] Bootstrap CI not significant
- [ ] Table 10 phase11 excerpt + 40 rows
- [ ] 63 pytest tests
- [ ] Qdrant vs Chroma latency comparison
- [ ] Cross-encoder nDCG 0.939 row
- [ ] Supplementary JSON/CSV regeneration

---

## V1.1 · Optional fast follow (between v1 and v2)

Small additions that do not require full v2 scope:

| Item | Effort |
|------|--------|
| `GET /agents/events/recent` + UI event strip | ~0.5 day |
| Qdrant backend switch (no phase11 yet) | ~1 day |
| Smoke benchmark script (5 queries, not full 30) | ~0.5 day |
| Copy `matching/*.py` lexical module only | ~1 day |

---

## Decision log (brainstorm 2026-05-27)

| Decision | Choice |
|----------|--------|
| ML v1 scope | Core only (no lexical, CE, bootstrap, full phase11) |
| Eval data | Copy from legacy repo |
| API | New routes + legacy aliases |
| Frontend | Full rewrite |
| Default strategy | Semantic cosine |
| Skills mode | Exposed in UI + API |
| Vector store v1 | Chroma only |
| Agent naming | Candidate Agent |
| Benchmark gate v1 | Smoke test only; regression in v2 |
| Paper timing | Code first, then manuscript |

---

## Implementation order (v1 only)

1. Copy `data/*.json` from legacy repo  
2. `contracts/` + `bus/` + `config.py`  
3. `core/` (document_text, embedding, scoring, skills, rrf, explain)  
4. `stores/` Chroma adapter  
5. Three agents + bootstrap  
6. API gateway + legacy aliases  
7. Frontend full rewrite  
8. Smoke test + unit/integration tests  

**Start v2 when:** v1 demo runs end-to-end (UI → three agents → ranked results) and supervisor approves demo for paper diagram update.

---

## Approval

| Reviewer | V1 scope OK | V2 scope OK | Date |
|----------|-------------|-------------|------|
| Harsh Kashyap | ☐ | ☐ | |
| Taranumpreet Kaur Wasu | ☐ | ☐ | |
| Dr Parteek Kumar | ☐ | ☐ | |
