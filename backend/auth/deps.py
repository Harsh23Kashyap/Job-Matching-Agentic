from typing import Callable

from fastapi import HTTPException, Request

from auth.store import User

SESSION_USER_KEY = "user_id"


def get_current_user(request: Request) -> User:
    user_id = request.session.get(SESSION_USER_KEY)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail={"error": "Not authenticated", "code": "UNAUTHORIZED"},
        )
    user = request.app.state.auth_store.get_by_id(user_id)
    if user is None:
        request.session.clear()
        raise HTTPException(
            status_code=401,
            detail={"error": "Session invalid", "code": "UNAUTHORIZED"},
        )
    return user


def get_optional_user(request: Request) -> User | None:
    user_id = request.session.get(SESSION_USER_KEY)
    if not user_id:
        return None
    return request.app.state.auth_store.get_by_id(user_id)


def require_role(*roles: str) -> Callable:
    allowed = frozenset(roles)

    def dependency(request: Request) -> User:
        user = get_current_user(request)
        if user.role not in allowed:
            raise HTTPException(
                status_code=403,
                detail={"error": "Insufficient permissions", "code": "FORBIDDEN"},
            )
        return user

    return dependency
