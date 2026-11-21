import threading
import time
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Session, select
from datetime import datetime
from src.core.db import get_session
from src.core.security import verify_password
from src.core.auth import create_access_token, get_current_user
from src.models.core import User, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])

# Manual in-memory login rate limiting (no external deps, offline-first).
# Keyed by username: after MAX_FAILED_ATTEMPTS within LOCKOUT_WINDOW seconds,
# further attempts for that account are rejected until the window rolls off.
_failed_attempts: dict[str, list[float]] = {}
_failed_attempts_lock = threading.Lock()
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_WINDOW_SECONDS = 15 * 60


def _is_locked_out(username: str) -> bool:
    now = time.monotonic()
    with _failed_attempts_lock:
        attempts = [t for t in _failed_attempts.get(username, []) if now - t < LOCKOUT_WINDOW_SECONDS]
        _failed_attempts[username] = attempts
        return len(attempts) >= MAX_FAILED_ATTEMPTS


def _record_failure(username: str) -> None:
    with _failed_attempts_lock:
        _failed_attempts.setdefault(username, []).append(time.monotonic())


def _clear_failures(username: str) -> None:
    with _failed_attempts_lock:
        _failed_attempts.pop(username, None)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserRead
    must_change_password: bool


@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """Authenticate a user and return an access token."""
    if _is_locked_out(form_data.username):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many failed login attempts. Try again in a few minutes.",
        )

    statement = select(User).where(User.username == form_data.username)
    user = session.exec(statement).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        _record_failure(form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    _clear_failures(form_data.username)

    # Update last login time
    user.last_login = datetime.utcnow()
    session.add(user)
    session.commit()
    session.refresh(user)

    access_token = create_access_token(subject=user.username)
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserRead.model_validate(user),
        must_change_password=user.must_change_password,
    )

@router.get("/me", response_model=UserRead)
def get_me(
    current_user: User = Depends(get_current_user)
):
    """Return the current authenticated user profile."""
    return current_user
