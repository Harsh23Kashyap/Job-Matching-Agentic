# Candidate portal pages

Job seeker flows: onboard → profile → find jobs → save & apply.

## Pages

| File | Route | Purpose |
|------|-------|---------|
| `Onboarding.jsx` | `/candidate/onboarding` | Resume upload + review stepper; AI extract with manual fallback |
| `Profile.jsx` | `/candidate/profile` | Edit profile; re-upload resume |
| `Matches.jsx` | `/candidate/matches` | Find/refresh job matches; profile gate via `fetchMyProfileOrNull` |
| `Saved.jsx` | `/candidate/saved` | Bookmarked jobs |

## Key behaviors

- **Profile upsert** — always `PUT /candidates/me` via `upsertCandidateProfile()`
- **Jobs unlock** — `isCandidateProfileReady()` after GET `/candidates/me`
- **Match drawer** — score breakdown, skill gaps, resume coach, similar jobs
- **Refresh** — refetch profile on `PROFILE_UPDATED_EVENT` and tab visibility

## Default match

`DEFAULT_CANDIDATE_MATCH` in [../api/client.js](../api/client.js) uses `strategy: "composite"`.

Demo: sign in as `demo.candidate@test.com` → linked to Rahul Sharma → instant matches.
