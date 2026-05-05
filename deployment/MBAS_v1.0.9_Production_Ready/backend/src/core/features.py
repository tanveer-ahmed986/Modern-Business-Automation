from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime
from src.core.db import get_session
from src.models.core import Settings
from src.core.license import get_license_validator

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
        # Check if license is still valid (not expired)
        validator = get_license_validator()
        if validator:
            license_info = validator.get_license_info()
            if license_info and license_info.expiry_date:
                if datetime.utcnow() > license_info.expiry_date:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="License expired. Please renew your license to continue using this feature."
                    )

        # Check feature flag
        flags = settings.feature_flags or {}
        if not flags.get(feature_name, False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Feature '{feature_name}' is not enabled in your current package. Upgrade to Standard or Premium to access this feature."
            )
        return True
    return feature_checker

def is_feature_enabled(session: Session, feature_name: str) -> bool:
    """Check if a feature is enabled without raising an exception."""
    settings = session.exec(select(Settings).where(Settings.id == 1)).first()
    if not settings:
        return False
    flags = settings.feature_flags or {}
    return flags.get(feature_name, False)
