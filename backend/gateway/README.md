# Gateway

Thin FastAPI layer — HTTP routes delegate to agents and stores. No business logic beyond request validation and auth.

## Files

| File | Purpose |
|------|---------|
| `app.py` | `build_gateway()` — mounts routers, session middleware, demo seed |
| `middleware.py` | `ReadOnlyMiddleware` — blocks mutating routes when `READ_ONLY=true` |

## Routes

All HTTP endpoints live in [routes/](routes/README.md).

## App state

| Attribute | Contents |
|-----------|----------|
| `app.state.container` | `SystemContainer` (agents, bus, settings) |
| `app.state.auth_store` | `UserStore` |
| `app.state.feedback_store` | Portal feedback SQLite |
| `app.state.activity_store` | Saved jobs, applications |
| `app.state.demo_accounts` | Seeded demo user IDs (if `SEED_DEMO=true`) |
