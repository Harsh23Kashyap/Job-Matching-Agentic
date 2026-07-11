# JAAMAS figure designs (review before draw.io)

**Workflow:** Review Mermaid here → approve each figure → export to `source/FigN.drawio` → `python3 scripts/generate_jaamas_figures.py` → check `FigN.pdf` → `\JFigure` in manuscript.

**Rules:** Grayscale in final PDF; agent names match Section 3–Section 5; one idea per figure; dashed = read/event/optional, solid = owned path.

**Color policy:** Mermaid previews in this doc use **color for review only** (flowcharts via `classDef`; sequence diagrams use the default theme for Markdown preview compatibility). draw.io export for `FigN.pdf` converts to **grayscale** for Springer/JAAMAS print.

| Role | Preview color | Portal / agent |
|------|---------------|----------------|
| Sage green | `#d1e7dd` | Candidate agent & portal |
| Sand/warm | `#f3ebe0` | Employer agent & portal |
| Slate blue | `#e6ebf0` | Matchmaking agent |
| Sky blue | `#dbeafe` | UI layer |
| Violet | `#ede9fe` | Shared events / snapshots |
| Amber | `#fef3c7` | Optional / external API |
| Mint store | `#f0fdf4` | Vector stores |
| Gray auth | `#f1f5f9` | Auth / SQLite |

**Status key:** `draft` | `approved` | `drawio` | `done`

---

## Architecture ladder (professor spec)

Read figures **top-down** in Section 3, simple → per-agent → full detail.

| Fig | Name | Where in paper | Purpose |
|-----|------|----------------|---------|
| **1** | **HLD (simple)** | Start of Section 3 | 3 agents + 2 portals + users; one glance |
| **2** | **Candidate agent (expanded)** | Section 3.1 | Inner components of candidate-side agent |
| **3** | **Employer agent (expanded)** | Section 3.2 | Inner components of employer-side agent |
| **4** | **Matchmaking agent (expanded)** | Section 3.3 | Inner components of read-only matcher |
| **5** | **Full block architecture (detailed)** | End of Section 3 (before Section 3.4 comms) | All agents + stores + gateway + bus in one diagram |
| 6 | Candidate workflow (sequence) | Section 3.5 | End-user path |
| 7 | Employer workflow (sequence) | Section 3.5 | Mirror of Fig 6 |
| 8 | Matching pipeline | Section 4 | Implementation scoring path |
| 9 | Evaluation pipeline | Section 5 | Benchmark / regression |

**Manuscript:** `\JFigure` refs updated in `section-3/4/5 .tex`, Fig 1 HLD → Figs 2–4 agents → Fig 5 capstone → Figs 6–7 workflows → Figs 8–9 pipelines.

---

## Fig 1, HLD simple (Section 3 opening) `approved → synced source/Fig1.mmd → exported Fig1.png`

**Caption:** High-level view of JobMatch: two market-side agents own candidate and job state; a read-only Matchmaking agent scores pairings and returns explained rankings to role-specific portals.

**Rules:** Max **9 boxes**, no inner pipelines, no library names.

**Portal UI (footnote):** Onboarding stepper → profile form → quality panel on candidate side; JD import → job form on employer side.

```mermaid
flowchart LR
  subgraph CAND["Candidate side"]
    direction TB
    JS(["Job seeker"])
    CP("Candidate portal")
    CA("Candidate agent<br/>owns candidate state")
    JS --> CP --> CA
  end

  subgraph CORE["Platform core"]
    direction TB
    AD("Admin / evaluation")
    MA("Matchmaking agent<br/>read-only broker")
    AD -.->|evaluation| MA
  end

  subgraph EMP["Employer side"]
    direction TB
    EM(["Employer / recruiter"])
    EP("Employer portal")
    EA("Employer agent<br/>owns job state")
    EM --> EP --> EA
  end

  CA <-->|events and snapshots| MA
  EA <-->|events and snapshots| MA
  MA -->|ranked matches| CP
  MA -->|ranked candidates| EP

  classDef actor fill:#eef2ff,stroke:#4338ca,color:#1e1b4b,stroke-width:1.5px
  classDef portal fill:#f8fafc,stroke:#475569,color:#0f172a,stroke-width:1.5px
  classDef agentC fill:#ecfdf5,stroke:#047857,color:#064e3b,stroke-width:1.5px
  classDef agentE fill:#fffbeb,stroke:#b45309,color:#78350f,stroke-width:1.5px
  classDef broker fill:#eff6ff,stroke:#1d4ed8,color:#1e3a8a,stroke-width:2px
  classDef admin fill:#faf5ff,stroke:#7c3aed,color:#4c1d95,stroke-width:1px

  class JS,EM actor
  class CP,EP portal
  class CA agentC
  class EA agentE
  class MA broker
  class AD admin
```

**Review checklist**
- [x] Readable in 10 seconds
- [x] Only three agent boxes (no sub-components)
- [x] Agent ↔ matchmaking data flow clear (snapshots + invalidation events)

---

## Fig 2, Candidate agent expanded (Section 3.1) `approved → synced source/Fig2.mmd`

**Caption:** Internal structure of the Candidate/Client agent: document ingestion (clean, rule extract, optional LLM merge), skill normalization, profile quality check, editable profile vs match-ready snapshot, embedding, and side outputs (events, activity store, resume coach).

**Portal UI (footnote):** `Onboarding.jsx` stepper → `ProfileForm.jsx` → `ProfileQualityScore.jsx`.

```mermaid
flowchart TB
  subgraph IN["Inputs"]
    direction LR
    UP("Resume upload / edit")
    FORM("Portal profile form")
  end

  subgraph PARSE["Ingestion pipeline"]
    direction LR
    CLEAN("Text clean")
    RULES("Rule extract")
    CONTACT("Contact extract")
    NORM("Profile normalize")
    SK("Skill catalog + taxonomy")
    QC("Profile quality check")
    CLEAN --> RULES --> CONTACT --> NORM --> SK --> QC
  end

  LLM("Optional LLM merge")

  subgraph STATE["Owned state"]
    direction LR
    PROF("Profile editable")
    SNAP("Snapshot match-ready")
    VAL("Schema validate")
    MEM("In-memory profiles")
    BOOT[("Bootstrap cvs.json")]
  end

  OWN("Ownership link")

  subgraph VEC["Representation"]
    direction LR
    TMPL("Document text template")
    EMB("Embedder MiniLM")
    VS[("Candidate vector index")]
    TMPL --> EMB --> VS
  end

  subgraph OUT["Outputs"]
    direction LR
    EVT("profile-updated event")
    UI("Confirmed fields to portal")
    COACH("Resume coach read-only")
    ACT[("Saved jobs + applications")]
  end

  UP --> CLEAN
  FORM --> NORM
  LLM -.-> NORM
  QC --> PROF
  QC --> SNAP
  SNAP --> VAL --> MEM
  BOOT -.-> MEM
  SNAP --> TMPL
  SNAP --> EVT
  PROF --> UI
  OWN -.-> MEM
  SNAP -.-> COACH
  UI -.-> ACT

  classDef input fill:#eef2ff,stroke:#4338ca,color:#1e1b4b,stroke-width:1.5px
  classDef parse fill:#ecfdf5,stroke:#047857,color:#064e3b,stroke-width:1.5px
  classDef state fill:#d1fae5,stroke:#059669,color:#065f46,stroke-width:1.5px
  classDef store fill:#f0fdf4,stroke:#166534,color:#14532d,stroke-width:1.5px
  classDef auth fill:#f8fafc,stroke:#64748b,color:#334155,stroke-width:1.5px
  classDef vec fill:#eff6ff,stroke:#2563eb,color:#1e3a8a,stroke-width:1.5px
  classDef out fill:#faf5ff,stroke:#7c3aed,color:#4c1d95,stroke-width:1.5px
  classDef opt fill:#fffbeb,stroke:#d97706,color:#92400e,stroke-width:1.5px

  class UP,FORM input
  class CLEAN,RULES,CONTACT,NORM,SK,QC parse
  class PROF,SNAP,VAL,MEM state
  class BOOT,VS,ACT store
  class OWN auth
  class TMPL,EMB vec
  class EVT,UI out
  class LLM,COACH opt
```

**Review checklist**
- [x] Snapshot vs editable profile distinction visible
- [x] No arrows to employer store
- [x] Event emitted only after snapshot commit
- [x] Bootstrap JSON dashed (not live write path)

---

## Fig 3, Employer agent expanded (Section 3.2) `approved → synced source/Fig3.mmd`

**Caption:** Internal structure of the Employer agent: JD ingestion (clean, rules, optional LLM), job quality check, posting status lifecycle, optional external feed sync, job snapshots, and side outputs (events, applicants feed, similar candidates).

```mermaid
flowchart TB
  subgraph IN["Inputs"]
    direction LR
    PASTE("JD paste")
    FILE("File upload")
    FORM("Job posting form")
    LIVE("External jobs API optional")
  end

  subgraph PARSE["Ingestion pipeline"]
    direction LR
    CLEAN("Text clean")
    RULES("Rule extract")
    NORM("Job field normalize")
    SK("Required skills extract")
    JQ("Job quality check")
    CLEAN --> RULES --> NORM --> SK --> JQ
  end

  LLM("Optional LLM merge")

  subgraph SYNC["Live sync optional"]
    direction LR
    FETCH("Fetch + normalize")
    SNAPFILE[("jobs_live.json")]
    REPL("Replace corpus + re-embed")
    FETCH --> SNAPFILE --> REPL
  end

  subgraph STATE["Owned state"]
    direction LR
    POST("Editable posting")
    STAT("Status open closed draft")
    SNAP("Versioned job snapshot")
    MEM("In-memory jobs")
    BOOT[("Bootstrap jobs.json")]
  end

  subgraph VEC["Representation"]
    direction LR
    TMPL("Document text template")
    EMB("Embedder MiniLM")
    VS[("Job vector index")]
    TMPL --> EMB --> VS
  end

  subgraph OUT["Outputs"]
    direction LR
    EVT("job-updated event")
    UI("Posting UI")
    APPL("Applicants feed read-only")
    SIM("Similar candidates")
  end

  PASTE --> CLEAN
  FILE --> CLEAN
  FORM --> NORM
  LLM -.-> NORM
  LIVE -.-> FETCH
  REPL -.-> NORM
  JQ --> POST
  JQ --> STAT
  JQ --> SNAP
  SNAP --> MEM
  BOOT -.-> MEM
  SNAP --> TMPL
  SNAP --> EVT
  POST --> UI
  UI --> APPL
  SNAP -.-> SIM

  classDef input fill:#fffbeb,stroke:#b45309,color:#78350f,stroke-width:1.5px
  classDef parse fill:#fef3c7,stroke:#d97706,color:#92400e,stroke-width:1.5px
  classDef sync fill:#fde68a,stroke:#ca8a04,color:#713f12,stroke-width:1.5px
  classDef state fill:#fef9c3,stroke:#a16207,color:#78350f,stroke-width:1.5px
  classDef store fill:#f0fdf4,stroke:#166534,color:#14532d,stroke-width:1.5px
  classDef vec fill:#eff6ff,stroke:#2563eb,color:#1e3a8a,stroke-width:1.5px
  classDef out fill:#faf5ff,stroke:#7c3aed,color:#4c1d95,stroke-width:1.5px
  classDef opt fill:#fff7ed,stroke:#ea580c,color:#9a3412,stroke-width:1.5px

  class PASTE,FILE,FORM input
  class LIVE opt
  class CLEAN,RULES,NORM,SK,JQ parse
  class FETCH,SNAPFILE,REPL sync
  class POST,STAT,SNAP,MEM state
  class BOOT,VS store
  class TMPL,EMB vec
  class EVT,UI,APPL out
  class LLM,SIM opt
```

**Review checklist**
- [x] Live API path dashed/optional with full sync chain
- [x] Symmetric layout with Fig 2
- [x] Does not write candidate data
- [x] Job status lifecycle visible

---

## Fig 4, Matchmaking agent expanded (Section 3.3) `approved`

**Caption:** Internal structure of the read-only Matchmaking agent: retrieval (exhaustive or ANN; lexical eval-only), composite scoring (28/27/10/15/10/10 weights including title fit), feasibility constraints, optional fusion/rerank/calibration/feedback boost, rule or LLM explanations, and session invalidation log.

**API paths (footnote):** `/match/ensemble` (RRF), `/match/daily-batch` for batch recommendations.

```mermaid
flowchart TB
  subgraph IN["Read-only inputs"]
    CS["Candidate snapshot ID"]
    JS["Job snapshot set"]
    EVT["Invalidation events"]
  end

  subgraph RET["Retrieval"]
    EXH["Exhaustive demo default"]
    ANN["Vector ANN search"]
    LEX["Lexical BM25 eval only"]
  end

  subgraph SCORE["Default composite strategy"]
    SEM["Semantic 28%"]
    SKL["Skills 27%"]
    TIT["Title fit 10%"]
    EXP["Experience 15%"]
    PAY["Compensation 10%"]
    REM["Remote 10%"]
    COMP["Weighted final score"]
  end

  subgraph POST["Post-score"]
    CON["Feasibility constraints"]
  end

  subgraph OPT["Optional branches"]
    ROUTE["Auto strategy router"]
    RRF["RRF fusion"]
    XENC["Cross-encoder rerank"]
    CAL["Calibration"]
    FDB["Feedback boost"]
  end

  subgraph EXPL["Explanation"]
    JSON["Structured JSON"]
    RULE["Rule explainer default"]
    GLLM["Grounded LLM explainer"]
  end

  subgraph OUT["Outputs"]
    RANK["Ranked list"]
    SESS["Invalidation flag + session log"]
    SIM["Similar jobs / candidates"]
  end

  CS --> EXH
  CS --> ANN
  JS --> EXH
  JS --> ANN
  EVT -.-> SESS
  LEX -.-> COMP
  EXH --> COMP
  ANN --> COMP
  SEM --> COMP
  SKL --> COMP
  TIT --> COMP
  EXP --> COMP
  PAY --> COMP
  REM --> COMP
  COMP --> CON
  CON --> RANK
  CON --> JSON
  JSON --> RULE
  GLLM -.-> JSON
  ROUTE -.-> COMP
  CON -.-> RRF
  RRF -.-> XENC
  XENC -.-> CAL
  CAL -.-> RANK
  FDB -.-> CON
  RANK --> SESS
  RANK -.-> SIM

  classDef input fill:#e6ebf0,stroke:#4a5d72,color:#1e293b
  classDef ret fill:#dbeafe,stroke:#2563eb,color:#1e3a5f
  classDef score fill:#d1e7dd,stroke:#52635a,color:#1a2e24
  classDef post fill:#ecfdf5,stroke:#059669,color:#064e3b
  classDef opt fill:#fef3c7,stroke:#d97706,color:#78350f
  classDef expl fill:#ede9fe,stroke:#6d28d9,color:#3b0764
  classDef out fill:#e6ebf0,stroke:#4a5d72,color:#1e293b

  class CS,JS,EVT input
  class EXH,ANN ret
  class LEX,ROUTE,RRF,XENC,CAL,FDB,GLLM,SIM opt
  class SEM,SKL,TIT,EXP,PAY,REM,COMP score
  class CON post
  class JSON,RULE expl
  class RANK,SESS out
```

**Review checklist**
- [x] All inputs labeled read-only
- [x] Default path solid; optional dashed
- [x] Title fit (10%) in composite
- [x] Constraints + explainer fork explicit
- [x] Lexical marked eval-only

---

## Fig 5, Full detailed block architecture (Section 3 capstone) `approved`

**Caption:** End-to-end block diagram: three portals (candidate, employer, admin console sub-zones), API gateway with auth and read-only middleware, three agents (abbreviated from Figs 2–4), persistence layer (SQLite, bootstrap JSON, vectors), shared platform, feedback loop, and vector backends (Chroma/Qdrant).

*Superset of Figs 2–4, every agent box maps to an expanded figure.*

**Admin console sub-zones:** agent health, event strip, vector switch, demo reset, live jobs sync, fairness snapshot, match eval controls.

```mermaid
flowchart TB
  subgraph UI["Application layer"]
    CP["Candidate portal"]
    EP["Employer portal"]
    AD["Admin console"]
  end

  subgraph GW["API gateway"]
    AUTH["Auth sessions roles"]
    RO["ReadOnly middleware"]
    API["REST handlers"]
  end

  subgraph AGCA["Candidate agent Fig 2"]
    C1["Parse pipeline"]
    C2["Profile + snapshot"]
    CVS[("Candidate vectors")]
    CACT[("Activity SQLite")]
  end

  subgraph AGEA["Employer agent Fig 3"]
    E1["Parse + live sync"]
    E2["Job + snapshot + status"]
    JVS[("Job vectors")]
    ELIVE["Live jobs sync"]
  end

  subgraph AGMA["Matchmaking agent Fig 4"]
    M1["Retrieve composite constraints"]
    M2["Explain + rank"]
    MSESS["Invalidation + session log"]
  end

  subgraph PERSIST["Persistence"]
    SQL[("SQLite users ownership feedback activity")]
    BOOT[("Bootstrap JSON cvs jobs")]
    LIVE[("jobs_live snapshot")]
  end

  subgraph SHARED["Shared platform"]
    CAT[("Skill catalog")]
    BUS["Event bus"]
    SNAP["Snapshot contracts"]
    ML[("fusion calibration models")]
  end

  subgraph FB["Feedback loop"]
    ACT["Portal save apply dismiss"]
    FAPI["feedback actions API"]
  end

  subgraph VEC["Vector backends"]
    CH["Chroma"]
    QD["Qdrant"]
  end

  CP --> AUTH
  EP --> AUTH
  AD --> AUTH
  AUTH --> RO --> API
  API --> C1
  API --> E1
  API --> M1
  C1 --> C2 --> CVS
  C2 --> CACT
  E1 --> E2 --> JVS
  ELIVE -.-> E1
  LIVE -.-> E1
  BOOT -.-> C2
  BOOT -.-> E2
  API --> SQL
  CP -.-> ACT
  EP -.-> ACT
  ACT --> FAPI --> SQL
  FAPI -.-> M1
  CVS -.-> M1
  JVS -.-> M1
  C2 --> SNAP
  E2 --> SNAP
  C2 -.-> BUS
  E2 -.-> BUS
  BUS -.-> MSESS
  M1 --> M2 --> API
  CAT --> C1
  CAT --> E1
  ML -.-> M1
  CVS --- CH
  CVS --- QD
  JVS --- CH
  JVS --- QD

  classDef ui fill:#dbeafe,stroke:#2563eb,color:#1e3a5f
  classDef gw fill:#f1f5f9,stroke:#64748b,color:#0f172a
  classDef candidate fill:#d1e7dd,stroke:#52635a,color:#1a2e24
  classDef employer fill:#f3ebe0,stroke:#7a6348,color:#3d2f1f
  classDef match fill:#e6ebf0,stroke:#4a5d72,color:#1e293b
  classDef persist fill:#f0fdf4,stroke:#166534,color:#14532d
  classDef shared fill:#ede9fe,stroke:#6d28d9,color:#3b0764
  classDef fb fill:#fce7f3,stroke:#be185d,color:#500724
  classDef vec fill:#e0f2fe,stroke:#0284c7,color:#0c4a6e
  classDef ext fill:#fef3c7,stroke:#d97706,color:#78350f

  class CP,EP,AD ui
  class AUTH,API,RO gw
  class C1,C2,CACT,CVS candidate
  class E1,E2,ELIVE,JVS employer
  class M1,M2,MSESS match
  class SQL,BOOT,LIVE persist
  class CAT,BUS,SNAP shared
  class ML,ELIVE,LIVE ext
  class ACT,FAPI fb
  class CH,QD vec
```

**Review checklist**
- [x] Superset of Figs 2–4 (professor can map boxes)
- [x] Gateway + auth + read-only middleware visible
- [x] SQLite + feedback loop separate from vectors
- [x] Bootstrap vs runtime distinguished
- [x] Vector backend switch shown

---

## Fig 6, Candidate workflow (Section 3.5) `approved → synced source/Fig6.mmd`

**Caption:** Candidate workflow: resume upload, assisted parsing, quality check and form prefill, profile confirmation with ownership link, snapshot registration, vector upsert, ranked job discovery with explanation drawer, and explicit save/apply/dismiss actions recorded to the feedback store.

```mermaid
sequenceDiagram
  autonumber
  actor C as Candidate
  participant UI as Candidate portal
  participant CA as Candidate agent
  participant MA as Matchmaking agent
  participant VS as Vector store
  participant FB as Feedback store

  C->>UI: Upload / edit resume
  UI->>CA: Raw document + edits
  CA->>CA: Parse, normalize
  CA->>CA: Quality check
  CA->>UI: Extracted fields for review
  C->>UI: Confirm profile
  UI->>CA: Commit profile + snapshot
  CA->>CA: Ownership link + schema validate
  CA->>VS: Upsert embeddings
  CA->>MA: Snapshot / invalidation event
  MA->>VS: Read jobs + candidate vector
  MA->>MA: Score, rank, explain
  MA->>UI: Ranked job list + breakdown drawer
  opt Resume coach
    C->>UI: Open job detail
    UI->>CA: Resume suggestions read-only
    CA->>UI: Improvement tips
  end
  C->>UI: Save / apply / dismiss
  UI->>FB: recordFeedbackAction
```

**Review checklist**
- [x] Human confirmation step before matching
- [x] Quality check → form prefill explicit
- [x] Explanation drawer on results
- [x] Save/apply/dismiss → feedback store (not auto-apply)
- [x] Optional resume coach path

---

## Fig 7, Employer workflow (Section 3.5) `approved → synced source/Fig7.mmd`

**Caption:** Employer workflow: JD ingestion, job quality check, posting confirmation with status open, snapshot registration, reverse candidate matching with explanation drawer, feedback actions (save/reject/contact), and applicants page review.

```mermaid
sequenceDiagram
  autonumber
  actor E as Employer
  participant UI as Employer portal
  participant EA as Employer agent
  participant MA as Matchmaking agent
  participant VS as Vector store
  participant FB as Feedback store

  E->>UI: Paste / upload JD
  UI->>EA: Job draft
  EA->>EA: Parse, skills extract
  EA->>EA: Job quality check
  EA->>UI: Posting form prefill
  E->>UI: Confirm and publish status open
  UI->>EA: Job profile + snapshot
  EA->>VS: Upsert job embeddings
  EA->>MA: Snapshot / invalidation event
  MA->>VS: Read candidates + job vector
  MA->>MA: Score, rank, explain
  MA->>UI: Ranked candidates + breakdown drawer
  opt Similar candidates
    E->>UI: Open candidate detail
    UI->>MA: Similar candidates read-only
    MA->>UI: Related shortlist
  end
  E->>UI: Save / reject / contact
  UI->>FB: recordFeedbackAction
  E->>UI: Review applicants page
```

**Review checklist**
- [x] Symmetric structure with Fig 6
- [x] Job quality check + status=open
- [x] Explanation drawer + feedback terminal actions
- [x] Applicants page as parallel read path
- [x] No auto-hire language

---

## Fig 8, Matching pipeline (Section 4) `approved`

**Caption:** Implementation of the matching pipeline: retrieval (exhaustive or ANN primary; lexical benchmark-only), composite scoring with six weighted components (28/27/10/15/10/10), feasibility constraints, optional fusion/calibration/feedback boost/auto-strategy, and structured explanation fork (rule default, LLM optional) consumed by portal cards and drawer.

**Portal path callout:** Candidate and employer portals use fixed composite defaults; admin `MatchControls` exposes the full strategy matrix.

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    CAND["Candidate snapshot"]
    JOB["Job snapshot"]
  end

  subgraph RET["Retrieval"]
    EXH["Exhaustive"]
    ANN["ANN vector"]
    LEX["Lexical BM25 eval only"]
  end

  subgraph SCORE["Composite scoring default"]
    SEM["Semantic 28%"]
    SK["Skills 27%"]
    TIT["Title fit 10%"]
    EXP["Experience 15%"]
    PAY["Compensation 10%"]
    REM["Remote 10%"]
    W["Weighted final score"]
  end

  subgraph POST["Post-score"]
    CON["Feasibility constraints"]
  end

  subgraph OPT["Optional paths"]
    ROUTE["Auto strategy"]
    RRF["RRF / learned fusion"]
    CE["Cross-encoder rerank"]
    CAL["Score calibration"]
    FDB["Feedback boost"]
  end

  subgraph EXPL["Explanation"]
    EXPX["Structured JSON"]
    RULE["Rule bullets"]
    LLM["LLM bullets"]
  end

  subgraph OUT["Outputs"]
    RANK["Ranked list"]
    UI["Portal cards + drawer"]
  end

  CAND --> EXH
  CAND --> ANN
  JOB --> EXH
  JOB --> ANN
  CAND -.-> LEX
  JOB -.-> LEX
  EXH --> SEM
  ANN --> SEM
  LEX -.-> W
  SEM --> W
  SK --> W
  TIT --> W
  EXP --> W
  PAY --> W
  REM --> W
  W --> CON
  CON --> RANK
  CON --> EXPX
  EXPX --> RULE
  LLM -.-> EXPX
  ROUTE -.-> W
  CON -.-> RRF
  RRF -.-> CE
  CE -.-> CAL
  CAL -.-> RANK
  FDB -.-> CON
  RANK --> UI
  EXPX --> UI

  classDef input fill:#dbeafe,stroke:#2563eb,color:#1e3a5f
  classDef retrieve fill:#e0f2fe,stroke:#0284c7,color:#0c4a6e
  classDef score fill:#d1e7dd,stroke:#52635a,color:#1a2e24
  classDef post fill:#ecfdf5,stroke:#059669,color:#064e3b
  classDef optional fill:#fef3c7,stroke:#d97706,color:#78350f
  classDef expl fill:#ede9fe,stroke:#6d28d9,color:#3b0764
  classDef output fill:#e6ebf0,stroke:#4a5d72,color:#1e293b

  class CAND,JOB input
  class EXH,ANN retrieve
  class LEX optional
  class SEM,SK,TIT,EXP,PAY,REM,W score
  class CON post
  class ROUTE,RRF,CE,CAL,FDB optional
  class EXPX,RULE expl
  class LLM optional
  class RANK,UI output
```

**Review checklist**
- [x] Title fit in composite (6 components)
- [x] Constraints after composite
- [x] Explanation fork visible
- [x] Lexical dashed eval-only
- [x] Portal vs admin path noted in caption

---

## Fig 9, Evaluation pipeline (Section 5) `approved`

**Caption:** Quality evaluation pipeline: frozen demo corpus, benchmark drivers (baselines, progression, ablations, significance, explainability, cross-encoder report, negative mining), metric aggregation, fairness audits, optional ML training of fusion/calibration artifacts, regression gates, and paper tables. Evaluation runs via CLI/pytest only (no portal UI).

**Orchestrator (footnote):** `run_research_pipeline.py` wraps drivers in a 9-stage offline suite.

```mermaid
flowchart TB
  subgraph CORP["Frozen demo corpus"]
    CVS["30 resumes"]
    JBS["15 jobs"]
    PAIRS["47 graded relevance pairs"]
  end

  subgraph RUN["Benchmark drivers"]
    BASE["Baselines: TF-IDF, BM25, dense"]
    PROG["Progression: soft-embed, fusion, composite"]
    ABL["Ablations and hard negatives"]
    SIG["Significance tests"]
    XPL["Explainability eval"]
    CER["Cross-encoder report"]
    NM["Negative mining"]
  end

  subgraph ML["ML artifacts (optional)"]
    TRAIN["Train fusion + calibration"]
    MODELS[("data/models/")]
  end

  subgraph MET["Metrics"]
    P["P@5"]
    R["R@5"]
    N["nDCG@5"]
    LAT["Latency ms/query"]
  end

  subgraph AUD["Audits"]
    FN["Hard-negative label check"]
    FF["Synthetic fairness audit"]
    LIVE["Admin fairness snapshot"]
  end

  subgraph GATE["Regression gate"]
    EXP["expected/*.json baselines"]
    PYT["pytest test_eval_regression"]
  end

  subgraph OUT["Artifacts"]
    TBL["Paper tables Section 6"]
    JSON["benchmark_outputs/"]
  end

  CVS --> RUN
  JBS --> RUN
  PAIRS --> RUN
  RUN --> MET
  RUN --> AUD
  TRAIN -.-> MODELS
  MODELS -.-> PROG
  MET --> TBL
  AUD --> TBL
  MET --> JSON
  JSON --> EXP
  EXP --> PYT
  FF -.-> LIVE

  classDef corpus fill:#dbeafe,stroke:#2563eb,color:#1e3a5f
  classDef run fill:#d1e7dd,stroke:#52635a,color:#1a2e24
  classDef ml fill:#fef3c7,stroke:#d97706,color:#78350f
  classDef metrics fill:#e6ebf0,stroke:#4a5d72,color:#1e293b
  classDef audit fill:#fef3c7,stroke:#d97706,color:#78350f
  classDef gate fill:#ede9fe,stroke:#6d28d9,color:#3b0764
  classDef artifacts fill:#f3ebe0,stroke:#7a6348,color:#3d2f1f

  class CVS,JBS,PAIRS corpus
  class BASE,PROG,ABL,SIG,XPL,CER,NM run
  class TRAIN,MODELS ml
  class P,R,N,LAT metrics
  class FN,FF,LIVE audit
  class EXP,PYT gate
  class TBL,JSON artifacts
```

**Review checklist**
- [x] Numbers are corpus sizes, not results
- [x] Extended driver set (significance, explainability, CE, negative mining)
- [x] ML train path dashed
- [x] Admin fairness hook dashed
- [x] No eval UI, CLI/pytest only

---

## Out of scope for figures

Components present in the codebase but intentionally omitted from paper figures (document here only):

| Component | Reason omitted |
|-----------|----------------|
| Legacy route aliases (`/match-resume`, `/match-job`, etc.) | Implementation detail; canonical paths in Section 4 text |
| `parser_backend` config field | Unused at runtime |
| Orphan UI: `ProfileQualityPanel.jsx`, `ProfileStrength.jsx` | Not wired in current portal tree |
| Premium / 402 error page | No billing flow implemented |
| Full 50-endpoint API catalog | Listed in Section 4 prose, not as a figure |
| `rerank_diagnostics` telemetry | Internal CE timing logs only |
| Unused API client exports (`createApplication`, `updateSavedJob`, `recordFeedback`) | Portal uses `recordFeedbackAction` instead |

---

## Fig 1 (legacy), superseded by ladder above

<details>
<summary>Old single-shot architecture (merged into Fig 5)</summary>

**Caption (old manuscript):** Multi-agent architecture of the proposed JobMatch recruitment system…

See Fig 5 for the capstone block diagram with full inner components.

</details>

---

## Order of work (professor ladder)

1. **Fig 1 HLD**, approved → draw.io → PDF  
2. **Fig 2** Candidate agent → **Fig 3** Employer → **Fig 4** Matchmaking, approved  
3. **Fig 5** Full block architecture, approved  
4. **Fig 6–7** Workflows, approved  
5. **Fig 8–9** Pipeline + evaluation, approved  
6. Export all to draw.io → regenerate PDFs → verify manuscript `\JFigure` paths

## Preview Mermaid locally

Open this file in VS Code with a Mermaid preview extension, or paste a block into [mermaid.live](https://mermaid.live).

After approval, sync approved diagram to `source/FigN.mmd` and regenerate draw.io via `scripts/generate_jaamas_figures.py` (or hand-edit `.drawio`).

**Quick export (all figures):**
```bash
cd docs/submission/jaamas/figures
bash export_all_mermaid.sh
```

## Readability guardrails (draw.io export)

- **Fig 1:** ≤9 boxes
- **Figs 2–4:** ≤18 boxes each; use subgraphs
- **Fig 5:** ≤28 boxes in zones; abbreviate vs Figs 2–4
- **Fig 8:** LR layout; optional paths dashed
- **All PDFs:** grayscale; color only in markdown preview
