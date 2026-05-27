from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from auth.routes import router as auth_router
from auth.store import UserStore
from bootstrap import SystemContainer
from gateway.routes import agents, candidates, employers, matching, system


def build_gateway(container: SystemContainer) -> FastAPI:
    app = FastAPI(title="Job Matching Multi-Agent System", version="1.1.0")
    app.state.container = container
    app.state.auth_store = UserStore(container.settings.sqlite_path)

    app.add_middleware(
        SessionMiddleware,
        secret_key=container.settings.session_secret,
        session_cookie="jm_session",
        max_age=60 * 60 * 24 * 7,
        same_site="lax",
        https_only=False,
    )

    app.include_router(auth_router)
    app.include_router(agents.router)
    app.include_router(candidates.router)
    app.include_router(employers.router)
    app.include_router(matching.router)
    app.include_router(system.router)

    return app
