# Demo pre-flight checklist

Run this **30 minutes before** a supervisor or stakeholder demo.

## Environment

- [ ] Backend running on **port 8001** (`uvicorn main:create_app --factory --reload --port 8001`)
- [ ] Frontend running on **port 5173** (`npm run dev`)
- [ ] OpenAPI version is **2.0.0**: `curl -s http://localhost:8001/openapi.json | python3 -c "import sys,json; print(json.load(sys.stdin)['info']['version'])"`
- [ ] Tests green: `cd backend && pytest ../tests -q` (expect **116 passed**)

## Secrets (local only — never commit)

- [ ] `backend/.env` exists (copy from `backend/.env.example`)
- [ ] `OPENAI_API_KEY` set **or** Ollama running (`ollama serve`, model `llama3.2`) for resume upload demo
- [ ] `SESSION_SECRET` set to a non-default value if demoing on a shared machine

## Corpus bootstrap

- [ ] Admin console shows **~30 candidates** and **~15 jobs** (bootstrapped from `data/cvs.json` + `data/jobs.json`)
- [ ] Quick API smoke: Rahul Sharma → Machine Learning Engineer **rank 1**

```bash
curl -s -X POST http://localhost:8001/match/candidate-to-jobs \
  -H 'Content-Type: application/json' \
  -d '{"query_key":"Rahul Sharma","top_k":1,"strategy":"semantic","metric":"cosine"}' \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['results'][0]; print(r['rank'], r['target_label'])"
# Expected: 1 Machine Learning Engineer
```

## Demo accounts (optional — create fresh or reuse)

| Role | Email | Password |
|------|-------|----------|
| Candidate | `demo.candidate@test.com` | `demo1234` |
| Employer | `demo.employer@test.com` | `demo1234` |
| Admin | `demo.admin@test.com` | `demo1234` |

Register at http://localhost:5173/register if accounts don't exist yet.

## Browser

- [ ] Use a clean browser profile or incognito (avoids stale session cookies)
- [ ] Zoom / display at 100% — jobs table needs horizontal space on laptop screens

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
