# Frontend

React 19 + Vite 6 web app — role portals for candidate, employer, and admin.

## Run

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 (proxies API to backend on `:8001`).

## Build

```bash
npm run build    # output: frontend/dist/
npm run preview  # serve production build locally
```

## Source layout

All application code is under [src/](src/README.md).

| Path | Purpose |
|------|---------|
| `src/pages/` | Route-level portal pages |
| `src/components/` | Shared UI (drawer, forms, results, ornaments) |
| `src/api/` | Axios client and API helpers |
| `src/layouts/` | Portal shells and navigation |
| `src/utils/` | Profile/job field mapping, formatting, feedback state |
| `src/context/` | Auth provider |
| `vite.config.js` | Dev server, API proxy |

## Environment

Optional: `VITE_API_BASE_URL` — leave empty to use Vite proxy (default local setup).
