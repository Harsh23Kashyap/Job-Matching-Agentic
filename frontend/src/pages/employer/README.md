# Employer portal pages

Hiring team flows: post jobs → find candidates → review applicants.

## Pages

| File | Route | Purpose |
|------|-------|---------|
| `Jobs.jsx` | `/employer/jobs` | Paste or upload JD → extract → post/edit jobs |
| `Matches.jsx` | `/employer/matches` | Rank candidates for a selected job |
| `Applications.jsx` | `/employer/applications` | In-app applications from candidates |

## Key behaviors

- **JD ingest** — `parseJobDescriptionText()` or `uploadJobDescription()` then review `JobPostingForm`
- **Match drawer** — composite breakdown, contact links, similar candidates
- **Feedback** — save, reject, contact (persisted; ranking unchanged)

Demo: `demo.employer@test.com` has 5 pre-seeded jobs.

Components: [../../components/EmployerJobList.jsx](../../components/EmployerJobList.jsx), [../../components/EmployerCandidateResults.jsx](../../components/EmployerCandidateResults.jsx)
