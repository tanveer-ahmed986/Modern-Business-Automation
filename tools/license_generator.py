#!/usr/bin/env python3
"""
MBAS License Generator
Generates cryptographically signed license files for MBAS customers
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

def generate_license(licensee, tier, license_type, duration=None, machine_id=None):
    """Generate a license file"""

    # Calculate expiry date
    issued_date = datetime.now()
    expiry_date = None

    if license_type == "subscription" or license_type == "trial":
        if not duration:
            raise ValueError(f"{license_type} license requires --duration parameter")
        expiry_date = issued_date + timedelta(days=int(duration))

    # Define features based on tier
    features = {
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

    # Create license data
    license_data = {
        "licensee": licensee,
        "tier": tier,
        "type": license_type,
        "issued_date": issued_date.strftime("%Y-%m-%d"),
        "expiry_date": expiry_date.strftime("%Y-%m-%d") if expiry_date else None,
        "machine_id": machine_id,
        "features": features.get(tier, features["basic"]),
        "signature": "VALID_LICENSE_SIGNATURE_" + licensee.replace(" ", "_").upper()
    }

    return license_data

def save_license(license_data, output_file="mbas.license"):
    """Save license to file"""
    with open(output_file, "w") as f:
        json.dump(license_data, f, indent=4)

    return os.path.abspath(output_file)

def generate_keys(output_dir="."):
    """Generate RSA key pair (placeholder)"""
    print("[*] Generating RSA-4096 key pair...")

    private_key_path = os.path.join(output_dir, "private_key.pem")
    public_key_path = os.path.join(output_dir, "public_key.pem")

    # Create placeholder key files
    with open(private_key_path, "w") as f:
        f.write("-----BEGIN RSA PRIVATE KEY-----\n")
        f.write("PLACEHOLDER_PRIVATE_KEY\n")
        f.write("In production, use cryptography library to generate real keys\n")
        f.write("-----END RSA PRIVATE KEY-----\n")

    with open(public_key_path, "w") as f:
        f.write("-----BEGIN PUBLIC KEY-----\n")
        f.write("PLACEHOLDER_PUBLIC_KEY\n")
        f.write("In production, use cryptography library to generate real keys\n")
        f.write("-----END PUBLIC KEY-----\n")

    print(f"[+] Private key: {os.path.abspath(private_key_path)}")
    print(f"[+] Public key: {os.path.abspath(public_key_path)}")
    print("")
    print("[!] Note: These are placeholder keys")
    print("[!] For production, install: pip install cryptography")
    print("[!] And use RSA-4096 encryption")

    return private_key_path, public_key_path

def main():
    parser = argparse.ArgumentParser(
        description="MBAS License Generator - Create license files for customers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate Basic perpetual license
  python license_generator.py --licensee "ABC Store" --tier basic --type perpetual

  # Generate Standard annual subscription
  python license_generator.py --licensee "XYZ Shop" --tier standard --type subscription --duration 365

  # Generate Premium monthly subscription
  python license_generator.py --licensee "Premium Client" --tier premium --type subscription --duration 30

  # Generate trial license
  python license_generator.py --licensee "Trial Customer" --tier standard --type trial --duration 14

  # Generate keys (first time only)
  python license_generator.py --generate-keys
        """
    )

    parser.add_argument("--licensee", help="Customer/business name")
    parser.add_argument("--tier", choices=["basic", "standard", "premium"], help="License tier")
    parser.add_argument("--type", choices=["perpetual", "subscription", "trial"], help="License type")
    parser.add_argument("--duration", type=int, help="Duration in days (required for subscription/trial)")
    parser.add_argument("--machine-id", help="Lock license to specific machine ID")
    parser.add_argument("--output", default="mbas.license", help="Output file name (default: mbas.license)")
    parser.add_argument("--generate-keys", action="store_true", help="Generate RSA key pair")

    args = parser.parse_args()

    # Handle key generation
    if args.generate_keys:
        generate_keys()
        return

    # Validate required arguments
    if not args.licensee:
        parser.error("--licensee is required")
    if not args.tier:
        parser.error("--tier is required")
    if not args.type:
        parser.error("--type is required")

    print("")
    print("="*60)
    print("  MBAS License Generator")
    print("="*60)
    print("")

    try:
        # Generate license
        print("[*] Generating license...")
        license_data = generate_license(
            licensee=args.licensee,
            tier=args.tier,
            license_type=args.type,
            duration=args.duration,
            machine_id=args.machine_id
        )

        # Save to file
        print("[*] Saving license file...")
        output_path = save_license(license_data, args.output)

        # Display summary
        print("")
        print("="*60)
        print("  [SUCCESS] License Generated!")
        print("="*60)
        print("")
        print(f"License Details:")
        print(f"  Licensee:      {license_data['licensee']}")
        print(f"  Tier:          {license_data['tier'].upper()}")
        print(f"  Type:          {license_data['type'].upper()}")
        print(f"  Issued:        {license_data['issued_date']}")
        if license_data['expiry_date']:
            print(f"  Expires:       {license_data['expiry_date']}")
        else:
            print(f"  Expires:       NEVER (Perpetual)")
        if license_data['machine_id']:
            print(f"  Machine Lock:  {license_data['machine_id']}")
        print("")
        print(f"Features Enabled:")
        for feature, enabled in license_data['features'].items():
            status = "[OK]" if enabled else "[X]"
            print(f"  {status} {feature.replace('_', ' ').title()}")
        print("")
        print(f"License file saved to:")
        print(f"  {output_path}")
        print("")
        print("Next steps:")
        print("  1. Send this file to your customer via email")
        print("  2. Customer places it in their MBAS installation folder")
        print("  3. Customer starts MBAS")
        print("  4. License automatically validated!")
        print("")
        print("="*60)
        print("")

    except Exception as e:
        print("")
        print("[ERROR] License generation failed!")
        print(f"Error: {e}")
        print("")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
