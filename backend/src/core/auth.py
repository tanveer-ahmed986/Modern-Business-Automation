from datetime import datetime, timedelta
from typing import Optional, Any, Union
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from src.core.db import get_session
from src.models.core import User
from src.core.config import SECRET_KEY
import time
import threading

# JWT Configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120  # 2 hours for enhanced security with auto-logout

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

# In-memory user cache: {username: (User, timestamp)}
# Avoids querying the users table on every single API request.
# Protected by a lock since FastAPI handles concurrent requests.
_user_cache: dict[str, tuple[User, float]] = {}
_user_cache_lock = threading.Lock()
_USER_CACHE_TTL = 30  # seconds - short enough that a role/is_active edit
# takes effect quickly even if invalidate_user_cache() is missed somewhere.

def invalidate_user_cache(username: str) -> None:
    """Flush a cached user immediately after an admin changes their account
    (role, active flag, password, username) so the change takes effect on
    their very next request instead of waiting out the TTL."""
    with _user_cache_lock:
        _user_cache.pop(username, None)

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Generate a JWT token for user sessions."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """Validate token and return the subject (user_id/username)."""
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_jwt["sub"]
    except JWTError:
        return None

def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    """Dependency to retrieve the current authenticated user from the Authorization header."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    inactive_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="This account has been deactivated",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    username = verify_token(token)
    if username is None:
        raise credentials_exception

    # Check in-memory cache first (avoids DB query on every request)
    now = time.monotonic()
    with _user_cache_lock:
        cached = _user_cache.get(username)
    if cached and (now - cached[1]) < _USER_CACHE_TTL:
        if not cached[0].is_active:
            raise inactive_exception
        return cached[0]

    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()

    if user is None:
        with _user_cache_lock:
            _user_cache.pop(username, None)
        raise credentials_exception

    if not user.is_active:
        with _user_cache_lock:
            _user_cache.pop(username, None)
        raise inactive_exception

    # Cache the user object (detached from session via expire_on_commit=False)
    with _user_cache_lock:
        _user_cache[username] = (user, now)
    return user
