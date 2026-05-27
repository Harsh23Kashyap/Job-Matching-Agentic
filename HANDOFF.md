# Handoff
> Written: 2026-05-27 | Branch: main | Dir: /Users/harshkashyap/Projects/JobMatcher-v1/Job-Matching-Agentic

## Goal

Greenfield rewrite of **Agentic Job Matching** from a monolithic FastAPI API into a **three-agent multi-agent system** (Candidate Agent, Employer Agent, Matchmaking Agent) with event-driven in-process communication, full React UI, and core ML matching. Paper reframes from technical report to white paper (Sal Khan *Brave New Words* Part VIII narrative). **V1 implementation has not started** — design phase is complete and pushed to GitHub.

## Current state

- **Done:**
  - Git repo initialized and pushed: https://github.com/Harsh23Kashyap/Job-Matching-Agentic
  - HLD: `docs/design/HLD-multi-agent-system.md`
  - SDD: `docs/design/SDD-multi-agent-system.md` (~1095 lines)
  - V1/V2 scope: `docs/design/V1-V2-SCOPE.md`
  - Knowledge graph updated with paper rewrite roadmap + Khan Part VIII anchor (`.claude/knowledge_graph.md`)
  - Brainstorm decisions logged (`.claude/brainstorm-history.md`)
  - Commits: `40128bc` (first commit), `9cde892` (design docs)
- **In progress:** None — awaiting v1 implementation kickoff
- **Blocked:** No application code exists; `data/*.json` not yet copied from legacy repo

## Decisions made

| Decision | Why | Alternatives rejected |
|----------|-----|----------------------|
| Greenfield rewrite (not refactor in place) | Professor wants true agentic architecture; old `app.py` monolith hard to reframe | Paper-only rebrand; incremental refactor |
| Event-driven monolith (3 agent classes + in-process bus) | Credible MAS story without microservice ops | Request-response only; Redis/microservices from day one |
| Hybrid agentic: structured agents v1, LLM v2 | Ship demo fast; LLM parsing/explain later | LLM agents now (scope creep) |
| Preserve eval corpus + benchmarks only from legacy | Reproducible research; rewrite everything else | Port full backend; fresh data |
| V1 ML: core only (bi-encoder, Jaccard, soft embed, RRF, ANN) | 7–8 day target; benchmarks deferred | Full Table 9 parity in v1 |
| Chroma only in v1 | Simplicity | Qdrant switch day one |
| Default strategy: semantic cosine | Demo simplicity | Soft embed default (best nDCG but heavier) |
| Skills mode exposed in UI + API | Fixes old paper↔code gap; best ML result user-selectable | Jaccard-only v1 |
| Candidate Agent naming (not Client/Employee) | Consistent code + paper | Dual labels; Employee (professor wording) |
| New API routes + legacy aliases | Easier migration from old UI/benchmarks | New routes only; legacy primary |
| Full frontend rewrite | Agent status panel is core to demo narrative | Minimal panel on old App.jsx |
| Copy eval data from legacy repo | Byte-identical labels for future benchmark parity | Recreate schema |
| Code first, then paper manuscript | Working demo before §3 diagram | Paper before code |
| Benchmark regression gate deferred to v2 | User chose core_only ML scope | Hard gate on Table 9 floats |

## Open questions

- [ ] **Round 2 brainstorm skipped:** Which v1 agent workflows beyond basic match? (ensemble ✅ scoped, daily batch ✅, POST register ✅, real jobs ❌ v2, event log ❌ v2)
- [ ] **Legacy copy scope:** `data/*.json` only vs port `matching/*.py` into `core/` — V1-V2 doc says JSON only; confirm before implementation
- [ ] **Supervisor SDD sign-off:** Dr Parteek Bhatia approval on SDD before code — status unknown
- [ ] **SDD ML gaps:** Lexical, cross-encoder, bootstrap, phase11 parked v2 — add §5b to SDD or leave in V1-V2-SCOPE only?
- [ ] **Local legacy repo path:** Clone `github.com/Taranum01/Agentic-Job-Matching` or user has local copy?

## Blockers & dependencies

| What | Who/Where | Status |
|------|-----------|--------|
| Eval corpus `data/cvs.json`, `jobs.json`, `eval_pairs.json` | Legacy repo Taranum01/Agentic-Job-Matching | Not copied yet |
| SDD/HLD approval | Authors + supervisor | Informal proceed; checkboxes empty in docs |
| sentence-transformers + Chroma deps | pip install on implement | Not set up (no backend/) |

## Environment

- **Branch:** main
- **Uncommitted changes:** clean
- **Recent commits:**
  - `9cde892` Add SDD, V1/V2 scope, and design doc updates
  - `40128bc` first commit
- **Build status:** N/A (no code)
- **Test status:** not run
- **Active processes:** none

## What worked

- Event-driven monolith design maps 1:1 to professor's three-agent diagram
- Separating V1-V2-SCOPE.md prevents benchmark/LLM scope creep in first sprint
- Knowledge graph as persistent memory for legacy ML stack + paper traceability
- Brainstorm menu questions locked 8 key decisions before SDD ambiguity
- Git push succeeded after killing stuck GPG/commit hooks (use simple `git commit -m "msg"`)

## What didn't work

- First `git commit` with HEREDOC/trailer hung ~80s — retry with plain `-m` succeeded
- User skipped Round 2 brainstorm (workflows, benchmark gate, paper timing, legacy copy) — defaults applied in V1-V2-SCOPE
- Attempted "push the code" when no implementation exists — only design docs on remote

## Commands

```bash
# Clone / enter repo
cd /Users/harshkashyap/Projects/JobMatcher-v1/Job-Matching-Agentic

# Copy eval corpus from legacy (do this first in v1)
# git clone git@github.com:Taranum01/Agentic-Job-Matching.git /tmp/legacy-jm
# cp /tmp/legacy-jm/data/{cvs,jobs,eval_pairs}.json data/

# Future backend (not yet created)
# cd backend && python -m venv .venv && source .venv/bin/activate
# pip install fastapi uvicorn sentence-transformers chromadb pydantic numpy pytest
# uvicorn main:app --reload --port 8000

# Future frontend (not yet created)
# cd frontend && npm install && npm run dev

# Push after changes
git add -A && git commit -m "your message" && git push origin main
```

## Key files

| File | Why It Matters |
|------|---------------|
| `docs/design/V1-V2-SCOPE.md` | **Start here** — what's in v1 vs v2 |
| `docs/design/SDD-multi-agent-system.md` | Implementation spec: classes, API, tests, file layout |
| `docs/design/HLD-multi-agent-system.md` | Architecture narrative + agent definitions |
| `.claude/knowledge_graph.md` | Legacy system encyclopedia + paper rewrite + Khan Part VIII |
| `.claude/brainstorm-history.md` | Brainstorm decision index |
| `README.md` | Links to all design docs |

## External links

- Repo: https://github.com/Harsh23Kashyap/Job-Matching-Agentic
- Legacy source: https://github.com/Taranum01/Agentic-Job-Matching
- Khan framing: *Brave New Words* Part VIII (admissions → job matching parallel in knowledge graph §2b)

## Memory snapshot

- **Paper rewrite roadmap** (knowledge graph): white paper intro, no §1.x, three-agent §3, Sal Khan vision, contributions reworked
- **Best ML result (legacy):** soft skill embed @ w=0.7 → nDCG@5 0.969 (v1 exposes via skills_mode; benchmarks v2)
- **Professor checklist:** candidate + employer + matchmaking agents + UI + communication diagram

## Persistent context

- Knowledge graph: `.claude/knowledge_graph.md` (+ `.claude/knowledge_graph.json`)
- Approach notes: `.claude/brainstorm-history.md`
- Design specs: `docs/design/HLD-multi-agent-system.md`, `SDD-multi-agent-system.md`, `V1-V2-SCOPE.md`
- Memory index: none in repo

## Next steps

1. **Copy eval data** — `cp` legacy `data/{cvs,jobs,eval_pairs}.json` into `data/` — verify: 30 resumes, 15 jobs, 47 pairs loadable
2. **Implement v1 Step 1–3** per SDD §19: `backend/contracts/`, `bus/`, `config.py`, then `core/` — verify: pytest on contracts/bus passes
3. **Implement agents + bootstrap** — CandidateAgent, EmployerAgent, MatchmakingAgent, `create_system()` — verify: smoke test Rahul Sharma → ML Engineer rank 1
4. **API gateway + legacy aliases** — verify: `GET /agents/status` returns 3 agents; `POST /match-resume` works
5. **Frontend full rewrite** — AgentStatusPanel + MatchControls with skills_mode — verify: end-to-end match in browser
6. **Push + update paper §3 diagram** after demo works — verify: diagram matches implemented agent boundaries
