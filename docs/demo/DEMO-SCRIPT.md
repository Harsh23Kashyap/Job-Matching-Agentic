# JobMatch: 15-minute demo script

**Audience:** Supervisor / stakeholder  
**Goal:** Show v1.1 as a hiring product (portals + auth + explainable matches), not a debug console.  
**Pre-flight:** [DEMO-CHECKLIST.md](./DEMO-CHECKLIST.md)

---

## Narrative arc (one sentence)

> JobMatch is a three-agent system where candidates and employers use separate portals, while admins keep the full research console: matching blends semantic retrieval with skills, experience, compensation, and location into an explainable composite score.

---

## Part 1: Admin / research baseline (3 min)

**Login:** Register or sign in as **admin** → `/admin/console`

**Talking points:**
- Three agents: Candidate, Employer, Matchmaking. Each owns its data; matchmaking reads snapshots only.
- Corpus is bootstrapped (30 CVs, 15 jobs) for eval and demos.
- This console is for **research and benchmarking**; product users never see raw score decimals here without context.

**Live action:**
1. Open **Agent status**: confirm entity counts.
2. Select **Rahul Sharma**, strategy **semantic**, metric **cosine**, run match.
3. Point out **Machine Learning Engineer** at **rank 1** and `why_ranked` bullets in the technical results panel.

**Transition:** *"Candidates and employers get a simpler, product-facing experience: let me show the candidate portal."*

---

## Part 2: Candidate portal (5 min)

**Login:** Sign out → register/sign in as **candidate** (`demo.candidate@test.com` / `demo1234`)

**Talking points:**
- Onboarding: resume upload with automatic parsing and manual review.
- Profile includes contact links (email, phone, LinkedIn, portfolio) pulled from resume when possible.
- Jobs page ranks roles by fit with filters: no raw ML jargon.

**Live action:**
1. **Onboarding**: upload a PDF/DOCX resume *or* skip to manual entry.
2. On review step, show **Contact & links** section and **Skills** chips.
3. Save profile → go to **Jobs**.
4. Click **Find jobs** / **Refresh matches**.
5. Walk one row: match %, why it matches, skill chips.
6. Click **View details** drawer:
   - Overall match % and band (Strong / Good / Moderate / Low)
   - Score breakdown bars (semantic, skills, experience, compensation, location)
   - Matched skills and **missing skills** (gaps vs job requirements)
   - Short plain-language explanation

**Transition:** *"Employers post jobs and see the mirror view: ranked candidates for a role."*

---

## Part 3: Employer portal (4 min)

**Login:** Sign out → sign in as **employer** (`demo.employer@test.com` / `demo1234`)

**Talking points:**
- Employer owns job postings; matchmaking ranks candidates against required skills.
- Same explainability drawer: useful for shortlisting, not auto-hire.

**Live action:**
1. **Jobs** → paste a raw JD → **Extract details** (or upload PDF/DOCX) → review prefilled form → post role.
2. **Matches** → select the job → **Find candidates** / **Refresh matches**.
3. Show summary cards (profiles reviewed, good matches, top match %).
4. Open **View details** on the top candidate: composite breakdown, matched vs missing skills, contact links.

---

## Part 4: Architecture close (2 min)

**Optional:** Return to admin console or show HLD diagram in `docs/design/HLD-multi-agent-system.md`

**Talking points:**
- Event bus: profile updates invalidate match cache.
- Chroma vector store for semantic retrieval; exhaustive match over corpus in UI (v1 scale).
- v2 roadmap: benchmark parity (Table 9), LLM JD parser, Qdrant: see `docs/design/V1-V2-SCOPE.md`.

---

## Q&A prep

| Question | Answer |
|----------|--------|
| Is this production-ready? | v1.1 demo: auth is session cookie + SQLite; fine for research demo, not public deploy without hardening. |
| What if OpenAI is down? | Regex still extracts contact info; profile can be filled manually; LLM returns graceful fallback. |
| How is match score computed? | Portal default: **composite**: 28% semantic cosine, 27% skills overlap, 10% title overlap, 15% experience fit, 10% compensation alignment, 10% remote preference. Admin console can still run raw semantic-only for research. |
| Bias / fairness? | Acknowledged in docs; no automated fairness metrics in v1: human review required. |

---

## Timing cheat sheet

| Segment | Minutes |
|---------|---------|
| Admin smoke + agents | 3 |
| Candidate onboarding + jobs + drawer | 5 |
| Employer job + candidates + drawer | 4 |
| Architecture + Q&A buffer | 3 |
| **Total** | **~15** |
