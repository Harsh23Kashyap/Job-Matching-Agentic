# Demo pre-flight checklist

Run this **30 minutes before** a supervisor or stakeholder demo.

## Environment

- [ ] Backend running on **port 8001** (`uvicorn main:create_app --factory --reload --port 8001`)
- [ ] Frontend running on **port 5173** (`npm run dev`)
- [ ] OpenAPI version is **2.0.0**: `curl -s http://localhost:8001/openapi.json | python3 -c "import sys,json; print(json.load(sys.stdin)['info']['version'])"`
- [ ] Tests green: `cd backend && pytest ../tests -q` (expect **164 passed**)
- [ ] Node tests green: `node --test tests/unit/test_skills_input.mjs tests/unit/test_match_format.mjs` (expect **12 passed**)
- [ ] Frontend build: `cd frontend && npm run build`

## Secrets (local only: never commit)

- [ ] `backend/.env` exists (copy from `backend/.env.example`)
- [ ] `OPENAI_API_KEY` set **or** Ollama running (`ollama serve`, model `llama3.2`) for resume upload demo
- [ ] `SESSION_SECRET` set to a non-default value if demoing on a shared machine

## Corpus bootstrap

- [ ] Admin console shows **~30 candidates** and **~15 jobs** (bootstrapped from `data/cvs.json` + `data/jobs.json`)
- [ ] Quick API smoke: Rahul Sharma → Machine Learning Engineer **rank 1** (composite default)

```bash
# Composite match (portal default): expect rank 1 + score fields
curl -s -X POST http://localhost:8001/match/candidate-to-jobs \
  -H 'Content-Type: application/json' \
  -d '{"query_key":"Rahul Sharma","top_k":1,"strategy":"composite","metric":"cosine"}' \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['results'][0]; print(r['rank'], r['target_label'], round(r['final_score'],2))"

# Legacy semantic path still works
curl -s -X POST http://localhost:8001/match/candidate-to-jobs \
  -H 'Content-Type: application/json' \
  -d '{"query_key":"Rahul Sharma","top_k":1,"strategy":"semantic","metric":"cosine"}' \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['results'][0]; print(r['rank'], r['target_label'])"
# Expected: 1 Machine Learning Engineer
```

- [ ] Employer jobs smoke: `python3 scripts/smoke_employer_jobs.py` (expect 5 jobs for demo employer)
- [ ] JD paste parse (employer session): paste 40+ chars on **My Jobs → Import** or:

```bash
curl -s -X POST http://localhost:8001/auth/login -c /tmp/jm.txt \
  -H 'Content-Type: application/json' \
  -d '{"email":"demo.employer@test.com","password":"demo1234"}' > /dev/null
curl -s -X POST http://localhost:8001/jobs/parse-description -b /tmp/jm.txt \
  -H 'Content-Type: application/json' \
  -d '{"text":"Senior Python Developer at Acme. Skills: Python, FastAPI. 5+ years. Budget 80-100k USD. Remote full-time."}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); f=d.get('extracted_fields',{}); print(d.get('llm_status'), f.get('title')); assert f.get('title') or d.get('llm_status') in ('ok','unavailable')"
# Expected: ok + title (Ollama/OpenAI) or unavailable + partial fields (graceful fallback)
```

## Demo accounts (optional: create fresh or reuse)

Seeded automatically when the backend starts (`SEED_DEMO=true`, default). One-click login on http://localhost:5173/login.

| Role | Email | Password |
|------|-------|----------|
| Candidate (profile ready) | `demo.candidate@test.com` | `demo1234` |
| Employer (5 sample jobs) | `demo.employer@test.com` | `demo1234` |
| Admin | `demo.admin@test.com` | `demo1234` |

Candidate demo is linked to **Rahul Sharma**: Jobs → **Find matches** returns ranked roles immediately.

## Browser

- [ ] Use a clean browser profile or incognito (avoids stale session cookies)
- [ ] Zoom / display at 100%: jobs table needs horizontal space on laptop screens

## Fallbacks if something breaks

| Issue | Fallback |
|-------|----------|
| Resume LLM unavailable | Skip upload; use manual profile entry (onboarding step 2) |
| Match returns empty | Ensure profile saved with at least one skill; click **Refresh matches** |
| Port 8001 in use | Kill old uvicorn; restart backend |
| Vite stale error | `npm run build` (should pass); restart `npm run dev` |

## Post-demo

- [ ] Note any bugs or UX gaps in GitHub issues or HANDOFF.md
- [ ] Rotate API keys if demo was recorded or shared screen showed `.env`
