from fastapi import HTTPException, status
from sqlmodel import Session
from datetime import datetime
from src.core.license import get_license_validator
from src.models.license import get_tier_features


def get_effective_feature_flags() -> dict:
    """The AUTHORITATIVE source of truth for feature gating.

    Feature flags are derived from the signed license at runtime, never
    from the mutable `settings.feature_flags` DB column — that column is
    only a display mirror (refreshed from the license at startup) and must
    never be trusted for enforcement, since `PUT /settings/` is reachable
    by an Admin and would otherwise let anyone self-upgrade their tier.
    """
    validator = get_license_validator()
    if validator:
        license_info = validator.get_license_info()
        if license_info:
            if license_info.expiry_date and datetime.utcnow() > license_info.expiry_date:
                return get_tier_features("basic").model_dump()
            return license_info.features.model_dump()
    return get_tier_features("basic").model_dump()


def check_feature(feature_name: str):
    """Dependency factory to verify if a feature is enabled in the current tier."""
    def feature_checker():
        validator = get_license_validator()
        if validator:
            license_info = validator.get_license_info()
            if license_info and license_info.expiry_date:
                if datetime.utcnow() > license_info.expiry_date:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="License expired. Please renew your license to continue using this feature."
                    )

        flags = get_effective_feature_flags()
        if not flags.get(feature_name, False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Feature '{feature_name}' is not enabled in your current package. Upgrade to Standard or Premium to access this feature."
            )
        return True
    return feature_checker


def is_feature_enabled(session: Session, feature_name: str) -> bool:
    """Check if a feature is enabled without raising an exception.

    `session` is accepted for call-site compatibility but is unused: the
    license is the only authoritative source, same as check_feature().
    """
    flags = get_effective_feature_flags()
    return flags.get(feature_name, False)
