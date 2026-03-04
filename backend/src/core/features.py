from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from backend.src.core.db import get_session
from backend.src.models.core import Settings

def get_current_settings(session: Session = Depends(get_session)) -> Settings:
    """Dependency to retrieve the singleton settings row."""
    statement = select(Settings).where(Settings.id == 1)
    settings = session.exec(statement).first()
    if not settings:
        # Fallback if DB not bootstrapped correctly
        return Settings(id=1, feature_flags={})
    return settings

def check_feature(feature_name: str):
    """Dependency factory to verify if a feature is enabled in the current tier."""
    def feature_checker(settings: Settings = Depends(get_current_settings)):
        flags = settings.feature_flags or {}
        if not flags.get(feature_name, False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Feature '{feature_name}' is not enabled in your current package."
            )
        return True
    return feature_checker
