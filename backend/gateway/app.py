from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from auth.routes import router as auth_router
from auth.store import UserStore
from bootstrap import SystemContainer
from demo_seed import seed_demo_accounts
from gateway.middleware import ReadOnlyMiddleware
from gateway.routes import agents, candidates, employers, feedback, matching, similar, system


def build_gateway(container: SystemContainer) -> FastAPI:
    app = FastAPI(title="Job Matching Multi-Agent System", version="2.0.0")
    app.state.container = container
    app.state.auth_store = UserStore(container.settings.sqlite_path)
    app.state.feedback_store = container.feedback_store
    app.state.activity_store = container.activity_store

    if container.settings.seed_demo:
        app.state.demo_accounts = seed_demo_accounts(app.state.auth_store, container)
    else:
        app.state.demo_accounts = None

    app.add_middleware(ReadOnlyMiddleware)
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
    app.include_router(similar.router)
    app.include_router(feedback.router)
    app.include_router(system.router)

    return app
