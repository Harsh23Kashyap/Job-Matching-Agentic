from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field

from auth.deps import SESSION_USER_KEY, get_current_user
from auth.store import DuplicateEmailError, User, VALID_ROLES

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    role: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    role: str


def _to_response(user: User) -> UserResponse:
    return UserResponse(id=user.id, email=user.email, role=user.role)


@router.post("/register", status_code=201, response_model=UserResponse)
def register(body: RegisterRequest, request: Request):
    if body.role not in VALID_ROLES:
        raise HTTPException(
            status_code=400,
            detail={"error": "Invalid role", "code": "INVALID_ROLE"},
        )
    store = request.app.state.auth_store
    try:
        user = store.create_user(body.email, body.password, body.role)
    except DuplicateEmailError:
        raise HTTPException(
            status_code=409,
            detail={"error": "Email already registered", "code": "DUPLICATE_EMAIL"},
        ) from None
    request.session[SESSION_USER_KEY] = user.id
    return _to_response(user)


@router.post("/login", response_model=UserResponse)
def login(body: LoginRequest, request: Request):
    store = request.app.state.auth_store
    user = store.authenticate(body.email, body.password)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail={"error": "Invalid email or password", "code": "INVALID_CREDENTIALS"},
        )
    request.session[SESSION_USER_KEY] = user.id
    return _to_response(user)


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"ok": True}


@router.get("/me", response_model=UserResponse)
def me(request: Request):
    user = get_current_user(request)
    return _to_response(user)
