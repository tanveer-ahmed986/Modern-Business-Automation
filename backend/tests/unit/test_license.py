"""
Unit tests for License Validation System.

Tests RSA signature verification, expiry checks, and tamper detection.
"""

import pytest
import json
import base64
from pathlib import Path
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from src.core.license import LicenseValidator, LicenseValidationError
from src.models.license import LicenseData, get_tier_features


@pytest.fixture
def license_keys(tmp_path):
    """Create temporary license keys for testing."""
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.backends import default_backend

    # Generate key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,  # Smaller key for faster tests
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Save keys
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    private_key_path = tmp_path / "private_key.pem"
    public_key_path = tmp_path / "public_key.pem"

    private_key_path.write_bytes(private_pem)
    public_key_path.write_bytes(public_pem)

    return {
        "private_key": private_key,
        "public_key": public_key,
        "private_key_path": private_key_path,
        "public_key_path": public_key_path,
    }


@pytest.fixture
def signed_license(tmp_path, license_keys):
    """Create a signed license file for testing."""
    license_data = {
        "licensee": "Test Company",
        "tier": "premium",
        "issued_date": datetime.utcnow().isoformat(),
        "expiry_date": (datetime.utcnow() + timedelta(days=365)).isoformat(),
        "machine_id_hash": None,
        "features": get_tier_features("premium").model_dump()
    }

    # Sign the license
    message = json.dumps(license_data, sort_keys=True, separators=(',', ':')).encode('utf-8')
    signature = license_keys["private_key"].sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    license_data["signature"] = base64.b64encode(signature).decode('utf-8')

    license_path = tmp_path / "test.mbas-license"
    with open(license_path, 'w') as f:
        json.dump(license_data, f, indent=2)

    return {"path": license_path, "data": license_data}


@pytest.mark.unit
class TestLicenseValidation:
    """Test license validation logic."""

    def test_valid_license_passes(self, signed_license, license_keys):
        """Valid signed license should pass validation."""
        validator = LicenseValidator(
            str(signed_license["path"]),
            str(license_keys["public_key_path"])
        )

        license_info = validator.validate()

        assert license_info.licensee == "Test Company"
        assert license_info.tier == "premium"
        assert license_info.features.ai_assistant is True

    def test_missing_license_file_fails(self, tmp_path, license_keys):
        """Missing license file should raise error."""
        validator = LicenseValidator(
            str(tmp_path / "nonexistent.mbas-license"),
            str(license_keys["public_key_path"])
        )

        with pytest.raises(LicenseValidationError) as exc_info:
            validator.validate()

        assert "not found" in str(exc_info.value).lower()

    def test_missing_public_key_fails(self, signed_license, tmp_path):
        """Missing public key should raise error."""
        validator = LicenseValidator(
            str(signed_license["path"]),
            str(tmp_path / "nonexistent_public_key.pem")
        )

        with pytest.raises(LicenseValidationError) as exc_info:
            validator.validate()

        assert "public key" in str(exc_info.value).lower()

    def test_expired_license_fails(self, tmp_path, license_keys):
        """Expired license should fail validation."""
        expired_data = {
            "licensee": "Expired Company",
            "tier": "standard",
            "issued_date": (datetime.utcnow() - timedelta(days=400)).isoformat(),
            "expiry_date": (datetime.utcnow() - timedelta(days=1)).isoformat(),
            "machine_id_hash": None,
            "features": get_tier_features("standard").model_dump()
        }

        # Sign the expired license
        message = json.dumps(expired_data, sort_keys=True, separators=(',', ':')).encode('utf-8')
        signature = license_keys["private_key"].sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        expired_data["signature"] = base64.b64encode(signature).decode('utf-8')

        license_path = tmp_path / "expired.mbas-license"
        with open(license_path, 'w') as f:
            json.dump(expired_data, f)

        validator = LicenseValidator(
            str(license_path),
            str(license_keys["public_key_path"])
        )

        with pytest.raises(LicenseValidationError) as exc_info:
            validator.validate()

        assert "expired" in str(exc_info.value).lower()

    def test_perpetual_license_no_expiry(self, tmp_path, license_keys):
        """Perpetual license (no expiry_date) should pass validation."""
        perpetual_data = {
            "licensee": "Perpetual Company",
            "tier": "premium",
            "issued_date": datetime.utcnow().isoformat(),
            "expiry_date": None,  # Perpetual
            "machine_id_hash": None,
            "features": get_tier_features("premium").model_dump()
        }

        # Sign
        message = json.dumps(perpetual_data, sort_keys=True, separators=(',', ':')).encode('utf-8')
        signature = license_keys["private_key"].sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        perpetual_data["signature"] = base64.b64encode(signature).decode('utf-8')

        license_path = tmp_path / "perpetual.mbas-license"
        with open(license_path, 'w') as f:
            json.dump(perpetual_data, f)

        validator = LicenseValidator(
            str(license_path),
            str(license_keys["public_key_path"])
        )

        license_info = validator.validate()
        assert license_info.expiry_date is None


@pytest.mark.unit
class TestLicenseTampering:
    """Test tamper detection via signature verification."""

    def test_tampered_licensee_fails(self, signed_license, license_keys):
        """Modifying licensee name should invalidate signature."""
        # Read and modify license
        with open(signed_license["path"], 'r') as f:
            data = json.load(f)

        data["licensee"] = "Hacked Company"  # Tamper with licensee

        # Write back tampered license
        with open(signed_license["path"], 'w') as f:
            json.dump(data, f)

        validator = LicenseValidator(
            str(signed_license["path"]),
            str(license_keys["public_key_path"])
        )

        with pytest.raises(LicenseValidationError) as exc_info:
            validator.validate()

        assert "signature" in str(exc_info.value).lower() or "tampered" in str(exc_info.value).lower()

    def test_tampered_tier_fails(self, signed_license, license_keys):
        """Upgrading tier without proper signature should fail."""
        # Read and modify license
        with open(signed_license["path"], 'r') as f:
            data = json.load(f)

        # The signed fixture is already "premium" — change tier and licensee
        # to values that actually differ so the signature must break
        data["tier"] = "basic"
        data["licensee"] = "Tampered Company"

        # Write back without re-signing
        with open(signed_license["path"], 'w') as f:
            json.dump(data, f)

        validator = LicenseValidator(
            str(signed_license["path"]),
            str(license_keys["public_key_path"])
        )

        with pytest.raises(LicenseValidationError):
            validator.validate()

    def test_missing_signature_fails(self, signed_license, license_keys):
        """License without signature should fail."""
        with open(signed_license["path"], 'r') as f:
            data = json.load(f)

        del data["signature"]

        with open(signed_license["path"], 'w') as f:
            json.dump(data, f)

        validator = LicenseValidator(
            str(signed_license["path"]),
            str(license_keys["public_key_path"])
        )

        with pytest.raises(LicenseValidationError) as exc_info:
            validator.validate()

        assert "signature" in str(exc_info.value).lower()


@pytest.mark.unit
class TestTierFeatures:
    """Test tier-based feature flags."""

    def test_basic_tier_features(self):
        """Basic tier should have limited features."""
        features = get_tier_features("basic")

        assert features.inventory is True
        assert features.billing is True
        assert features.suppliers is False
        assert features.ai_assistant is False

    def test_standard_tier_features(self):
        """Standard tier should have intermediate features."""
        features = get_tier_features("standard")

        assert features.inventory is True
        assert features.suppliers is True
        assert features.backup_restore is True
        assert features.ai_assistant is False  # Premium only

    def test_premium_tier_features(self):
        """Premium tier should have all features."""
        features = get_tier_features("premium")

        assert features.inventory is True
        assert features.suppliers is True
        assert features.ai_assistant is True
        assert features.premium_reports is True
