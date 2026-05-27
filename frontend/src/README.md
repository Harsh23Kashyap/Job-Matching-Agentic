# Frontend source (`src/`)

React application entry and shared modules.

## Entry

| File | Role |
|------|------|
| `main.jsx` | React DOM mount |
| `App.jsx` | Router, auth provider, role-guarded routes |
| `App.css` | Design system · tokens, portal layouts, match drawer, dark mode |

## Subfolders

| Folder | README |
|--------|--------|
| `pages/` | [pages/README.md](pages/README.md) · portal routes |
| `components/` | [components/README.md](components/README.md) · reusable UI |
| `api/` | [api/README.md](api/README.md) · backend HTTP client |
| `layouts/` | [layouts/README.md](layouts/README.md) · shell chrome |
| `utils/` | [utils/README.md](utils/README.md) · helpers |
| `context/` | `AuthContext.jsx` · session user state |
| `hooks/` | `useTheme`, `useReducedMotion` |
| `constants/` | `demoAccounts.js` · demo email hints |

## Routing overview

| Role | Base path | Layout |
|------|-----------|--------|
| Candidate | `/candidate/*` | `CandidateLayout` |
| Employer | `/employer/*` | `EmployerLayout` |
| Admin | `/admin/*` | `AdminLayout` |
| Auth | `/login`, `/register` | `AuthLayout` |

Unauthenticated users redirect to `/login`. Wrong role → error page.
