# API client

Axios wrapper for backend communication. All requests use `withCredentials: true` for session cookies.

## Main file

`client.js` · exports used by pages and components.

## Key exports

| Function | Endpoint |
|----------|----------|
| `login`, `register`, `logout`, `fetchMe` | `/auth/*` |
| `fetchMyProfile`, `fetchMyProfileOrNull` | `GET /candidates/me` |
| `upsertCandidateProfile` | `PUT /candidates/me` |
| `uploadResume` | `POST /candidates/upload-resume` |
| `parseJobDescriptionText` | `POST /jobs/parse-description` |
| `runMatch` | `POST /match/candidate-to-jobs` or job-to-candidates |
| `submitFeedbackAction`, `fetchMyFeedback` | `/feedback/*` |
| `fetchSimilarJobs`, `fetchSimilarCandidates` | `/similar/*` |

## Defaults

```javascript
DEFAULT_CANDIDATE_MATCH = { strategy: "composite", top_k: 15, ... }
```

## Errors

`apiErrorMessage(err, fallback)` · parses FastAPI `detail` for form toasts.

Base URL: `import.meta.env.VITE_API_BASE_URL` or Vite dev proxy.
