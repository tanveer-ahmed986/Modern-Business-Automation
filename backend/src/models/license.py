"""License data models for MBAS package tiers."""

from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field


LicenseTier = Literal["basic", "standard", "premium"]


class LicenseFeatures(BaseModel):
    """Feature flags for different license tiers."""

    # Core features (all tiers)
    inventory: bool = True
    billing: bool = True
    customers: bool = True
    dashboard: bool = True

    # Standard and Premium features
    suppliers: bool = False
    purchases: bool = False
    backup_restore: bool = False
    advanced_reports: bool = False

    # Premium-only features
    premium_reports: bool = False
    ai_assistant: bool = False
    ai_forecasting: bool = False


class LicenseData(BaseModel):
    """License information and validation data."""

    licensee: str = Field(..., description="Business name of the licensee")
    tier: LicenseTier = Field(..., description="License tier (basic/standard/premium)")
    issued_date: datetime = Field(..., description="Date the license was issued")
    expiry_date: Optional[datetime] = Field(None, description="License expiration date (None = perpetual)")
    machine_id_hash: Optional[str] = Field(None, description="SHA256 hash of hardware ID for anti-piracy")
    features: LicenseFeatures = Field(..., description="Enabled features for this license")
    signature: str = Field(..., description="RSA signature for tamper detection")

    class Config:
        json_schema_extra = {
            "example": {
                "licensee": "ABC Retail Store",
                "tier": "premium",
                "issued_date": "2026-04-23T00:00:00",
                "expiry_date": "2027-04-23T00:00:00",
                "machine_id_hash": "a7b8c9d0e1f2...",
                "features": {
                    "inventory": True,
                    "billing": True,
                    "suppliers": True,
                    "premium_reports": True,
                    "ai_assistant": True
                },
                "signature": "base64_encoded_rsa_signature"
            }
        }


def get_tier_features(tier: LicenseTier) -> LicenseFeatures:
    """Get default feature set for a license tier."""

    if tier == "basic":
        return LicenseFeatures(
            inventory=True,
            billing=True,
            customers=True,
            dashboard=True,
            suppliers=False,
            purchases=False,
            backup_restore=False,
            advanced_reports=False,
            premium_reports=False,
            ai_assistant=False,
            ai_forecasting=False
        )
    elif tier == "standard":
        return LicenseFeatures(
            inventory=True,
            billing=True,
            customers=True,
            dashboard=True,
            suppliers=True,
            purchases=True,
            backup_restore=True,
            advanced_reports=True,
            premium_reports=False,
            ai_assistant=False,
            ai_forecasting=False
        )
    else:  # premium
        return LicenseFeatures(
            inventory=True,
            billing=True,
            customers=True,
            dashboard=True,
            suppliers=True,
            purchases=True,
            backup_restore=True,
            advanced_reports=True,
            premium_reports=True,
            ai_assistant=True,
            ai_forecasting=True
        )
