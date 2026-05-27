from fastapi import FastAPI

from bootstrap import SystemContainer
from gateway.routes import agents, candidates, employers, matching, system


def build_gateway(container: SystemContainer) -> FastAPI:
    app = FastAPI(title="Job Matching Multi-Agent System", version="1.0.0")
    app.state.container = container

    app.include_router(agents.router)
    app.include_router(candidates.router)
    app.include_router(employers.router)
    app.include_router(matching.router)
    app.include_router(system.router)

    return app
