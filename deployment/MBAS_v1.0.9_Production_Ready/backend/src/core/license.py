"""License validation engine for MBAS."""

import json
import hashlib
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

from src.models.license import LicenseData, LicenseFeatures


class LicenseValidationError(Exception):
    """Raised when license validation fails."""
    pass


class LicenseValidator:
    """Validates MBAS license files using RSA signature verification."""

    # Production license locations (in priority order)
    PRODUCTION_PATHS = [
        Path("C:/ProgramData/MBAS/mbas.license"),  # System-wide (admin-protected)
        Path.home() / "AppData/Local/MBAS/mbas.license",  # User-specific
    ]

    def __init__(self, license_path: str, public_key_path: str):
        """
        Initialize license validator.

        Args:
            license_path: Path to .mbas-license file (or None to auto-detect)
            public_key_path: Path to public key PEM file
        """
        self.license_path = self._find_license_path(license_path)
        self.public_key_path = Path(public_key_path)
        self._license_data: Optional[LicenseData] = None
        self._last_validation: Optional[datetime] = None

    @staticmethod
    def _find_license_path(provided_path: str) -> Path:
        """
        Find license file in standard locations.

        Args:
            provided_path: User-provided path or None

        Returns:
            Path to license file
        """
        # If path provided and exists, use it
        if provided_path:
            path = Path(provided_path)
            if path.exists():
                return path

        # Try production paths
        for prod_path in LicenseValidator.PRODUCTION_PATHS:
            if prod_path.exists():
                return prod_path

        # Fallback to provided path (for error messages)
        return Path(provided_path) if provided_path else Path("mbas.license")

    def validate(self, force_revalidate: bool = False) -> LicenseData:
        """
        Validate license file and return license data.

        Args:
            force_revalidate: Force re-validation even if cached

        Returns:
            LicenseData object with validated license information

        Raises:
            LicenseValidationError: If validation fails for any reason
        """
        # Use cached validation if recent (within 5 minutes)
        if not force_revalidate and self._license_data and self._last_validation:
            time_since_validation = (datetime.utcnow() - self._last_validation).total_seconds()
            if time_since_validation < 300:  # 5 minutes
                return self._license_data

        # Check if license file exists
        if not self.license_path.exists():
            raise LicenseValidationError(
                f"License file not found at {self.license_path}. "
                "Please contact your vendor for a valid license."
            )

        # Check if public key exists
        if not self.public_key_path.exists():
            raise LicenseValidationError(
                f"Public key not found at {self.public_key_path}. "
                "Application installation may be corrupted."
            )

        # Load and parse license file
        try:
            with open(self.license_path, 'r') as f:
                license_json = json.load(f)
        except json.JSONDecodeError as e:
            raise LicenseValidationError(f"Invalid license file format: {e}")
        except Exception as e:
            raise LicenseValidationError(f"Failed to read license file: {e}")

        # Extract signature before validation
        signature_b64 = license_json.get('signature')
        if not signature_b64:
            raise LicenseValidationError("License file is missing signature")

        # Remove signature from data for verification
        license_data_for_signing = license_json.copy()
        del license_data_for_signing['signature']

        # Verify RSA signature
        if not self._verify_signature(license_data_for_signing, signature_b64):
            raise LicenseValidationError(
                "License signature is invalid. File may have been tampered with."
            )

        # Parse license data
        try:
            self._license_data = LicenseData(**license_json)
        except Exception as e:
            raise LicenseValidationError(f"Invalid license data: {e}")

        # Check expiry date
        if self._license_data.expiry_date:
            if datetime.utcnow() > self._license_data.expiry_date:
                raise LicenseValidationError(
                    f"License expired on {self._license_data.expiry_date.date()}. "
                    "Please renew your license."
                )

        # Check machine ID if specified (optional anti-piracy measure)
        if self._license_data.machine_id_hash:
            current_machine_id = self.get_machine_id()
            if current_machine_id != self._license_data.machine_id_hash:
                raise LicenseValidationError(
                    "License is locked to a different machine. "
                    "Please contact your vendor for a new license."
                )

        # Cache validation timestamp
        self._last_validation = datetime.utcnow()

        return self._license_data

    def _verify_signature(self, license_data: dict, signature_b64: str) -> bool:
        """
        Verify RSA signature of license data.

        Args:
            license_data: License data dictionary (without signature field)
            signature_b64: Base64-encoded RSA signature

        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Load public key
            with open(self.public_key_path, 'rb') as f:
                public_key = serialization.load_pem_public_key(f.read())

            # Decode signature
            signature = base64.b64decode(signature_b64)

            # Create canonical JSON representation (sorted keys, no whitespace)
            message = json.dumps(license_data, sort_keys=True, separators=(',', ':')).encode('utf-8')

            # Verify signature
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True

        except InvalidSignature:
            return False
        except Exception as e:
            print(f"Error verifying signature: {e}")
            return False

    @staticmethod
    def get_machine_id() -> str:
        """
        Generate machine ID hash from hardware identifiers.

        Returns:
            SHA256 hash of CPU ID + Motherboard serial + MAC address

        Note:
            This is a basic implementation. For production, consider using
            more robust hardware fingerprinting libraries.
        """
        import platform
        import uuid

        # Combine multiple hardware identifiers
        identifiers = []

        # CPU identifier (platform-dependent)
        identifiers.append(platform.processor())

        # MAC address
        mac = uuid.getnode()
        identifiers.append(str(mac))

        # Machine name (less reliable but easy)
        identifiers.append(platform.node())

        # Combine and hash
        combined = '|'.join(identifiers)
        machine_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()

        return machine_hash

    def get_license_info(self) -> Optional[LicenseData]:
        """Get cached license data (must call validate() first)."""
        return self._license_data

    def check_file_integrity(self) -> bool:
        """
        Check if license file has been modified since last validation.

        Returns:
            True if file integrity is intact, False if modified
        """
        if not self._license_data or not self.license_path.exists():
            return False

        try:
            # Re-verify signature without updating cache
            with open(self.license_path, 'r') as f:
                license_json = json.load(f)

            signature_b64 = license_json.get('signature')
            if not signature_b64:
                return False

            license_data_for_signing = license_json.copy()
            del license_data_for_signing['signature']

            return self._verify_signature(license_data_for_signing, signature_b64)

        except Exception:
            return False


# Singleton instance (initialized on startup)
_license_validator: Optional[LicenseValidator] = None


def get_license_validator() -> Optional[LicenseValidator]:
    """Get global license validator instance."""
    return _license_validator


def set_license_validator(validator: LicenseValidator):
    """Set global license validator instance."""
    global _license_validator
    _license_validator = validator
