# Demo materials

Thesis and stakeholder demo (~15 minutes, three portals).

## Files

| File | Purpose |
|------|---------|
| [DEMO-SCRIPT.md](DEMO-SCRIPT.md) | Step-by-step narrative: admin → candidate → employer |
| [DEMO-CHECKLIST.md](DEMO-CHECKLIST.md) | Pre-flight: servers, corpus, demo accounts |

## Quick start

1. Start backend (`:8001`) and frontend (`:5173`)
2. Sign in `demo.candidate@test.com` / `demo1234` → Jobs → Find matches
3. Sign in `demo.employer@test.com` → paste JD → Extract → post → Candidates
4. Sign in `demo.admin@test.com` → match console → Rahul Sharma semantic match

Expected top match: **Rahul Sharma ↔ Machine Learning Engineer**.

## Paper screenshots

Automated capture for JAAMAS Figure 10 (requires running stack):

```bash
cd docs/submission/jaamas/figures/scripts && node capture_portal_screenshots.mjs
```
