from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

_READ_ONLY_ALLOWED = {"/auth/login", "/auth/register"}
_MUTATING_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


class ReadOnlyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in _MUTATING_METHODS:
            container = getattr(request.app.state, "container", None)
            if container is not None and container.settings.read_only:
                if request.url.path not in _READ_ONLY_ALLOWED:
                    return JSONResponse(
                        status_code=403,
                        content={
                            "detail": {
                                "error": "API is in read-only demo mode",
                                "code": "READ_ONLY",
                            }
                        },
                    )
        return await call_next(request)
