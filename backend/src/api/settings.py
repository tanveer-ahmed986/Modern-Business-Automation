from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime

from backend.src.core.db import get_session
from backend.src.models.core import Settings, User, UserRole
from backend.src.core.auth import get_current_user

router = APIRouter(prefix="/settings", tags=["settings"])

def check_admin_role(current_user: User = Depends(get_current_user)):
    """Dependency to ensure the current user has the ADMIN role."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation restricted to system administrators"
        )
    return current_user

@router.get("/", response_model=Settings)
def get_settings(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve the singleton system settings."""
    statement = select(Settings).where(Settings.id == 1)
    settings = session.exec(statement).first()
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings

@router.put("/", response_model=Settings)
def update_settings(
    *,
    session: Session = Depends(get_session),
    settings_in: Settings, # Using the model directly for simplicity since it's a singleton
    current_user: User = Depends(check_admin_role)
) -> Any:
    """Update system settings (Admin only)."""
    statement = select(Settings).where(Settings.id == 1)
    db_settings = session.exec(statement).first()
    if not db_settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    
    # Update only fields that are provided
    update_data = settings_in.dict(exclude_unset=True, exclude={"id"})
    for key, value in update_data.items():
        setattr(db_settings, key, value)
    
    db_settings.updated_at = datetime.utcnow()
    session.add(db_settings)
    session.commit()
    session.refresh(db_settings)
    return db_settings
