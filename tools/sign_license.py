#!/usr/bin/env python3
"""
MBAS License Signer - Creates properly signed license files
Uses RSA-4096 signature for tamper-proof licenses
"""

import json
import base64
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def sign_license_file(license_data: dict, private_key_path: str) -> str:
    """
    Sign license data with RSA private key.

    Args:
        license_data: Dictionary with license information (without signature)
        private_key_path: Path to private_key.pem

    Returns:
        Base64-encoded signature string
    """
    # Load private key
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    # Create canonical JSON (sorted keys, no whitespace)
    message = json.dumps(license_data, sort_keys=True, separators=(',', ':')).encode('utf-8')

    # Sign the message
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Encode as base64
    return base64.b64encode(signature).decode('utf-8')


def generate_license(
    licensee: str,
    tier: str,
    license_type: str,
    duration: int = None,
    machine_id: str = None,
    private_key_path: str = "tools/keys/private_key.pem"
) -> dict:
    """Generate and sign a license file."""

    # Calculate dates
    issued_date = datetime.now()
    expiry_date = None

    if license_type in ["subscription", "trial"]:
        if not duration:
            raise ValueError(f"{license_type} license requires duration parameter")
        expiry_date = issued_date + timedelta(days=int(duration))

    # Define features based on tier
    tier_features = {
        "basic": {
            "dashboard": True,
            "inventory": True,
            "billing": True,
            "customers": True,
            "suppliers": True,
            "purchases": True,
            "advanced_reports": False,
            "backup_restore": True,
            "ai_assistant": False,
            "premium_reports": False
        },
        "standard": {
            "dashboard": True,
            "inventory": True,
            "billing": True,
            "customers": True,
            "suppliers": True,
            "purchases": True,
            "advanced_reports": True,
            "backup_restore": True,
            "ai_assistant": False,
            "premium_reports": False
        },
        "premium": {
            "dashboard": True,
            "inventory": True,
            "billing": True,
            "customers": True,
            "suppliers": True,
            "purchases": True,
            "advanced_reports": True,
            "backup_restore": True,
            "ai_assistant": True,
            "premium_reports": True
        }
    }

    # Create license data (without signature)
    license_data = {
        "licensee": licensee,
        "tier": tier.lower(),
        "type": license_type,
        "issued_date": issued_date.strftime("%Y-%m-%d"),
        "expiry_date": expiry_date.strftime("%Y-%m-%d") if expiry_date else None,
        "machine_id_hash": machine_id,
        "features": tier_features.get(tier.lower(), tier_features["basic"])
    }

    # Sign the license
    print(f"[*] Signing license with private key: {private_key_path}")
    signature = sign_license_file(license_data, private_key_path)

    # Add signature
    license_data["signature"] = signature

    return license_data


def main():
    parser = argparse.ArgumentParser(
        description="MBAS License Signer - Create cryptographically signed licenses",
        epilog="""
Examples:
  # Generate Standard perpetual license
  python sign_license.py --licensee "ABC Pharmacy" --tier standard --type perpetual

  # Generate Premium annual subscription
  python sign_license.py --licensee "XYZ Hospital" --tier premium --type subscription --duration 365

  # Generate trial license
  python sign_license.py --licensee "Trial Customer" --tier standard --type trial --duration 14
        """
    )

    parser.add_argument("--licensee", required=True, help="Customer/business name")
    parser.add_argument("--tier", required=True, choices=["basic", "standard", "premium"], help="License tier")
    parser.add_argument("--type", required=True, choices=["perpetual", "subscription", "trial"], help="License type")
    parser.add_argument("--duration", type=int, help="Duration in days (required for subscription/trial)")
    parser.add_argument("--machine-id", help="Lock license to specific machine ID hash")
    parser.add_argument("--output", default="mbas.license", help="Output file (default: mbas.license)")
    parser.add_argument("--private-key", default="tools/keys/private_key.pem", help="Path to private key")

    args = parser.parse_args()

    print("")
    print("=" * 70)
    print("  MBAS License Signer - Cryptographically Signed Licenses")
    print("=" * 70)
    print("")

    try:
        # Generate signed license
        license_data = generate_license(
            licensee=args.licensee,
            tier=args.tier,
            license_type=args.type,
            duration=args.duration,
            machine_id=args.machine_id,
            private_key_path=args.private_key
        )

        # Save to file
        output_path = Path(args.output).resolve()
        with open(output_path, 'w') as f:
            json.dump(license_data, f, indent=4)

        print("[+] License generated and signed successfully!")
        print("")
        print("=" * 70)
        print("  License Details")
        print("=" * 70)
        print(f"  Licensee:      {license_data['licensee']}")
        print(f"  Tier:          {license_data['tier'].upper()}")
        print(f"  Type:          {license_data['type'].upper()}")
        print(f"  Issued:        {license_data['issued_date']}")
        if license_data['expiry_date']:
            print(f"  Expires:       {license_data['expiry_date']}")
        else:
            print(f"  Expires:       NEVER (Perpetual)")
        if license_data['machine_id_hash']:
            print(f"  Machine Lock:  {license_data['machine_id_hash']}")
        print("")
        print("  Features Enabled:")
        for feature, enabled in license_data['features'].items():
            status = "[YES]" if enabled else "[ NO]"
            print(f"    {status} {feature.replace('_', ' ').title()}")
        print("")
        print(f"  Signature:     {license_data['signature'][:50]}...")
        print("")
        print("=" * 70)
        print(f"  License saved to: {output_path}")
        print("=" * 70)
        print("")
        print("Next steps:")
        print("  1. Copy this file to the MBAS installation folder")
        print("  2. Place it next to START_MBAS.bat")
        print("  3. Restart MBAS - license will be automatically validated!")
        print("")

    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}")
        print("Make sure private_key.pem exists in tools/keys/")
        return 1
    except Exception as e:
        print(f"[ERROR] License generation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
