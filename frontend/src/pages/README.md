# Pages

Route-level components · one folder per portal role plus auth and errors.

## Portals

| Folder | Routes | README |
|--------|--------|--------|
| `candidate/` | onboarding, profile, matches, saved | [candidate/README.md](candidate/README.md) |
| `employer/` | jobs, matches, applications | [employer/README.md](employer/README.md) |
| `admin/` | console | [admin/README.md](admin/README.md) |

## Auth & errors

| File | Route |
|------|-------|
| `Login.jsx` | `/login` |
| `Register.jsx` | `/register` |
| `errors/ErrorPage.jsx` | `/error/:code` · forbidden, not found, etc. |

Route definitions: [../App.jsx](../App.jsx)
