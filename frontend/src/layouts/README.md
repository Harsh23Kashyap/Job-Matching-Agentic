# Layouts

Portal shells · sidebar/nav, background, user menu.

## Files

| File | Wraps |
|------|-------|
| `CandidateLayout.jsx` | `/candidate/*` routes |
| `EmployerLayout.jsx` | `/employer/*` routes |
| `AdminLayout.jsx` | `/admin/*` routes |
| `AuthLayout.jsx` | Login and register |
| `PortalShell.jsx` | Shared shell: nav items, header, `PortalBackground` |

Each layout uses `ProtectedRoute` with the matching role from [../context/AuthContext.jsx](../context/AuthContext.jsx).

Mobile: bottom nav on candidate/employer; admin uses top nav.
