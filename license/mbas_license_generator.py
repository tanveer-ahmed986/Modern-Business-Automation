#!/usr/bin/env python3
"""
MBAS License Generator - Self-Contained Interactive Tool
Generates RSA-4096 signed license files for MBAS customers.

Usage:
  Interactive:  python mbas_license_generator.py
  CLI mode:     python mbas_license_generator.py --licensee "ABC Store" --tier standard --type subscription --duration 180
  Gen keys:     python mbas_license_generator.py --generate-keys

Z&T Technologies - State-of-the-Art Business Solutions
"""

import json
import base64
import argparse
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# RSA Key Management
# ---------------------------------------------------------------------------

def ensure_cryptography():
    """Check if cryptography is installed, install if missing."""
    try:
        import cryptography  # noqa: F401
        return True
    except ImportError:
        print("[!] 'cryptography' package not found. Installing...")
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "cryptography"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            # pip might be broken, try ensurepip first
            subprocess.run(
                [sys.executable, "-m", "ensurepip", "--upgrade"],
                capture_output=True, text=True
            )
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "cryptography"],
                capture_output=True, text=True
            )
        if result.returncode == 0:
            print("[OK] 'cryptography' installed successfully.")
            return True
        else:
            print("[ERROR] Failed to install 'cryptography'.")
            print(result.stderr)
            return False


def find_keys_dir():
    """Locate the keys directory. Check multiple possible locations."""
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    candidates = [
        project_root / "tools" / "keys",
        script_dir / "keys",
    ]
    for d in candidates:
        if (d / "private_key.pem").exists():
            return d

    # Default to project_root/tools/keys (will be created if needed)
    return project_root / "tools" / "keys"


def generate_rsa_keys(keys_dir: Path):
    """Generate a new RSA-4096 key pair."""
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization

    print("[*] Generating RSA-4096 key pair (this may take a moment)...")
    keys_dir.mkdir(parents=True, exist_ok=True)

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)

    priv_path = keys_dir / "private_key.pem"
    pub_path = keys_dir / "public_key.pem"

    with open(priv_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(pub_path, "wb") as f:
        f.write(private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print(f"[OK] Private key saved: {priv_path}")
    print(f"[OK] Public key saved:  {pub_path}")
    print()
    print("[!] IMPORTANT: Keep private_key.pem SECRET. Never distribute it.")
    print("    Only public_key.pem should be included in client installations.")
    return priv_path, pub_path


def load_private_key(keys_dir: Path):
    """Load the RSA private key from disk."""
    from cryptography.hazmat.primitives import serialization

    priv_path = keys_dir / "private_key.pem"
    if not priv_path.exists():
        print(f"[!] Private key not found at: {priv_path}")
        print("[*] Generating new RSA-4096 key pair...")
        generate_rsa_keys(keys_dir)

    with open(priv_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    return private_key


# ---------------------------------------------------------------------------
# License Generation & Signing
# ---------------------------------------------------------------------------

TIER_FEATURES = {
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
        "premium_reports": False,
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
        "premium_reports": False,
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
        "premium_reports": True,
    },
}


def sign_data(private_key, data_dict: dict) -> str:
    """Sign license data with RSA-PSS and return base64 signature."""
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding

    message = json.dumps(data_dict, sort_keys=True, separators=(",", ":")).encode("utf-8")

    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return base64.b64encode(signature).decode("utf-8")


def build_license(licensee, tier, license_type, duration=None, machine_id=None):
    """Build the license data dict (without signature)."""
    issued = datetime.now()
    expiry = None

    if license_type in ("subscription", "trial"):
        if not duration:
            raise ValueError(f"{license_type} license requires a duration (days).")
        expiry = issued + timedelta(days=int(duration))

    return {
        "licensee": licensee,
        "tier": tier.lower(),
        "type": license_type,
        "issued_date": issued.strftime("%Y-%m-%d"),
        "expiry_date": expiry.strftime("%Y-%m-%d") if expiry else None,
        "machine_id_hash": machine_id if machine_id else None,
        "features": TIER_FEATURES.get(tier.lower(), TIER_FEATURES["basic"]),
    }


def generate_and_sign(licensee, tier, license_type, duration=None, machine_id=None, keys_dir=None):
    """Full pipeline: build license data, sign with RSA, return complete dict."""
    if keys_dir is None:
        keys_dir = find_keys_dir()

    private_key = load_private_key(keys_dir)
    license_data = build_license(licensee, tier, license_type, duration, machine_id)

    print("[*] Signing license with RSA-4096 private key...")
    signature = sign_data(private_key, license_data)
    license_data["signature"] = signature

    return license_data


def save_license(license_data: dict, output_path: Path):
    """Write license JSON to file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(license_data, f, indent=4)
    return output_path.resolve()


def print_license_summary(license_data: dict, output_path):
    """Display a formatted summary of the generated license."""
    print()
    print("=" * 70)
    print("  LICENSE GENERATED SUCCESSFULLY")
    print("=" * 70)
    print()
    print(f"  Licensee:      {license_data['licensee']}")
    print(f"  Tier:          {license_data['tier'].upper()}")
    print(f"  Type:          {license_data['type'].upper()}")
    print(f"  Issued:        {license_data['issued_date']}")
    if license_data["expiry_date"]:
        print(f"  Expires:       {license_data['expiry_date']}")
    else:
        print(f"  Expires:       NEVER (Perpetual)")
    if license_data.get("machine_id_hash"):
        print(f"  Machine Lock:  {license_data['machine_id_hash']}")
    print()
    print("  Features Enabled:")
    for feature, enabled in license_data["features"].items():
        status = "[YES]" if enabled else "[ NO]"
        print(f"    {status} {feature.replace('_', ' ').title()}")
    print()
    sig_preview = license_data["signature"][:50]
    print(f"  RSA Signature: {sig_preview}...")
    print()
    print("=" * 70)
    print(f"  Saved to: {output_path}")
    print("=" * 70)
    print()


# ---------------------------------------------------------------------------
# Interactive Mode
# ---------------------------------------------------------------------------

def ask_choice(prompt, options, allow_custom=False):
    """Ask user to pick from numbered options. Returns the value."""
    while True:
        for i, (label, _value) in enumerate(options, 1):
            print(f"  {i}. {label}")
        if allow_custom:
            print(f"  {len(options)+1}. Custom (enter manually)")
        print()
        try:
            raw = input(prompt).strip()
            idx = int(raw)
            if 1 <= idx <= len(options):
                return options[idx - 1][1]
            if allow_custom and idx == len(options) + 1:
                return "custom"
        except (ValueError, EOFError):
            pass
        print("  [!] Invalid choice. Try again.\n")


def interactive_mode():
    """Run the full interactive license generation wizard."""
    print()
    print("=" * 70)
    print("  MBAS LICENSE GENERATOR - Interactive Mode")
    print("  Z&T Technologies - State-of-the-Art Business Solutions")
    print("=" * 70)
    print()

    # --- Step 1: Tier ---
    print("STEP 1: SELECT LICENSE TIER")
    print("-" * 40)
    print()
    tier = ask_choice("Enter choice (1-3): ", [
        ("Basic Edition       - Dashboard, Inventory, Billing, Reports, Backup", "basic"),
        ("Standard Edition    - All Basic + Advanced Reports, Multi-user", "standard"),
        ("Premium Edition     - All Standard + AI Forecasting, Premium Analytics", "premium"),
    ])
    tier_display = tier.capitalize()
    print(f"  -> Selected: {tier_display}\n")

    # --- Step 2: License Type ---
    print("STEP 2: SELECT LICENSE TYPE")
    print("-" * 40)
    print()
    license_type = ask_choice("Enter choice (1-3): ", [
        ("Perpetual (Lifetime)    - No expiration, one-time payment", "perpetual"),
        ("Subscription (Recurring)- Expires after duration, requires renewal", "subscription"),
        ("Trial (Free Trial)      - Limited time, full features for evaluation", "trial"),
    ])
    type_display = license_type.capitalize()
    print(f"  -> Selected: {type_display}\n")

    # --- Step 3: Duration ---
    duration = None
    if license_type == "subscription":
        print("STEP 3: SELECT SUBSCRIPTION DURATION")
        print("-" * 40)
        print()
        dur_choice = ask_choice("Enter choice (1-5): ", [
            ("1 Month    (30 days)", 30),
            ("3 Months   (90 days)", 90),
            ("6 Months   (180 days)", 180),
            ("1 Year     (365 days)", 365),
        ], allow_custom=True)

        if dur_choice == "custom":
            while True:
                try:
                    raw = input("  Enter number of days (1-3650): ").strip()
                    duration = int(raw)
                    if 1 <= duration <= 3650:
                        break
                    print("  [!] Must be between 1 and 3650.")
                except (ValueError, EOFError):
                    print("  [!] Enter a valid number.")
        else:
            duration = dur_choice
        print(f"  -> Duration: {duration} days\n")

    elif license_type == "trial":
        print("STEP 3: SET TRIAL DURATION")
        print("-" * 40)
        print()
        dur_choice = ask_choice("Enter choice (1-4): ", [
            ("7 days", 7),
            ("14 days", 14),
            ("30 days", 30),
        ], allow_custom=True)

        if dur_choice == "custom":
            while True:
                try:
                    raw = input("  Enter trial days (1-365): ").strip()
                    duration = int(raw)
                    if 1 <= duration <= 365:
                        break
                    print("  [!] Must be between 1 and 365.")
                except (ValueError, EOFError):
                    print("  [!] Enter a valid number.")
        else:
            duration = dur_choice
        print(f"  -> Trial duration: {duration} days\n")

    else:
        print("STEP 3: DURATION")
        print("-" * 40)
        print("  Perpetual license - no expiration date.")
        print()

    # --- Step 4: Business Name ---
    print("STEP 4: BUSINESS INFORMATION")
    print("-" * 40)
    print()
    print("  Enter the customer's business name.")
    print("  Examples: ABC Pharmacy, XYZ Electronics, City Retail Center")
    print()
    while True:
        try:
            business_name = input("  Business name: ").strip()
            if business_name:
                break
            print("  [!] Business name cannot be empty.")
        except EOFError:
            print("  [!] Input required.")
    print(f"  -> Business: {business_name}\n")

    # --- Step 5: Hardware Lock (optional) ---
    print("STEP 5: HARDWARE LOCK (Optional)")
    print("-" * 40)
    print()
    print("  Lock license to a specific computer?")
    print("  This prevents the license from being used on other machines.")
    print()
    machine_id = None
    try:
        lock = input("  Lock to hardware? (Y/N) [N]: ").strip().upper()
    except EOFError:
        lock = "N"

    if lock == "Y":
        print()
        print("  Enter the machine ID hash.")
        print("  The customer can get their machine ID by running:")
        print('    python -c "from src.core.license import LicenseValidator; print(LicenseValidator.get_machine_id())"')
        print()
        try:
            machine_id = input("  Machine ID (or press Enter to skip): ").strip()
        except EOFError:
            machine_id = ""
        if not machine_id:
            machine_id = None
            print("  -> No hardware lock.\n")
        else:
            print(f"  -> Machine ID: {machine_id}\n")
    else:
        print("  -> No hardware lock.\n")

    # --- Step 6: Output file ---
    print("STEP 6: OUTPUT FILE")
    print("-" * 40)
    print()
    script_dir = Path(__file__).resolve().parent
    default_output = script_dir / "mbas.license"
    print(f"  Default output: {default_output}")
    try:
        custom_out = input(f"  Output file (press Enter for default): ").strip()
    except EOFError:
        custom_out = ""
    if custom_out:
        output_path = Path(custom_out)
    else:
        output_path = default_output
    print(f"  -> Output: {output_path}\n")

    # --- Confirmation ---
    print("=" * 70)
    print("  CONFIRMATION")
    print("=" * 70)
    print()
    print(f"  Business Name: {business_name}")
    print(f"  Tier:          {tier_display}")
    print(f"  Type:          {type_display}")
    if duration:
        print(f"  Duration:      {duration} days")
    if machine_id:
        print(f"  Machine Lock:  {machine_id}")
    print(f"  Output:        {output_path}")
    print()

    try:
        confirm = input("  Generate license? (Y/N): ").strip().upper()
    except EOFError:
        confirm = "N"

    if confirm != "Y":
        print("\n  License generation cancelled.\n")
        return 0

    # --- Generate ---
    print()
    print("  Generating RSA-4096 signed license...")
    print()

    license_data = generate_and_sign(
        licensee=business_name,
        tier=tier,
        license_type=license_type,
        duration=duration,
        machine_id=machine_id,
    )

    saved_path = save_license(license_data, output_path)
    print_license_summary(license_data, saved_path)

    print("  Next steps:")
    print("    1. Send mbas.license to the customer (email, USB, etc.)")
    print("    2. Customer places it in their MBAS installation folder")
    print("    3. Customer starts MBAS - license is validated automatically")
    print()

    # Ask to generate another
    try:
        another = input("  Generate another license? (Y/N) [N]: ").strip().upper()
    except EOFError:
        another = "N"
    if another == "Y":
        return interactive_mode()

    print()
    print("  Thank you for using MBAS License Generator!")
    print()
    return 0


# ---------------------------------------------------------------------------
# CLI Mode
# ---------------------------------------------------------------------------

def cli_mode(args):
    """Non-interactive command-line mode."""
    print()
    print("=" * 70)
    print("  MBAS License Signer - CLI Mode")
    print("=" * 70)
    print()

    keys_dir = None
    if args.private_key:
        keys_dir = Path(args.private_key).parent

    license_data = generate_and_sign(
        licensee=args.licensee,
        tier=args.tier,
        license_type=args.type,
        duration=args.duration,
        machine_id=getattr(args, "machine_id", None),
        keys_dir=keys_dir,
    )

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = Path.cwd() / output_path

    saved_path = save_license(license_data, output_path)
    print_license_summary(license_data, saved_path)
    return 0


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="MBAS License Generator - RSA-4096 Signed Licenses",
        epilog="""
Examples:
  Interactive mode (recommended):
    python mbas_license_generator.py

  CLI - Standard perpetual license:
    python mbas_license_generator.py --licensee "ABC Pharmacy" --tier standard --type perpetual

  CLI - Premium 6-month subscription:
    python mbas_license_generator.py --licensee "XYZ Hospital" --tier premium --type subscription --duration 180

  CLI - Premium 1-year subscription:
    python mbas_license_generator.py --licensee "City Clinic" --tier premium --type subscription --duration 365

  CLI - Trial license (custom days):
    python mbas_license_generator.py --licensee "Demo Customer" --tier standard --type trial --duration 30

  Generate new RSA keys:
    python mbas_license_generator.py --generate-keys
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--licensee", help="Customer/business name")
    parser.add_argument("--tier", choices=["basic", "standard", "premium"], help="License tier")
    parser.add_argument("--type", choices=["perpetual", "subscription", "trial"], help="License type")
    parser.add_argument("--duration", type=int, help="Duration in days (required for subscription/trial)")
    parser.add_argument("--machine-id", dest="machine_id", help="Lock to specific machine ID hash")
    parser.add_argument("--output", default="mbas.license", help="Output file (default: mbas.license)")
    parser.add_argument("--private-key", help="Path to private_key.pem (auto-detected by default)")
    parser.add_argument("--generate-keys", action="store_true", help="Generate new RSA-4096 key pair")

    args = parser.parse_args()

    # Ensure cryptography is available
    if not ensure_cryptography():
        print("\n[ERROR] Cannot proceed without the 'cryptography' package.")
        print("  Install manually: pip install cryptography")
        return 1

    # Key generation mode
    if args.generate_keys:
        keys_dir = find_keys_dir()
        print()
        generate_rsa_keys(keys_dir)
        print()
        return 0

    # If no licensee provided, go interactive
    if not args.licensee:
        return interactive_mode()

    # Validate CLI args
    if not args.tier:
        parser.error("--tier is required in CLI mode")
    if not args.type:
        parser.error("--type is required in CLI mode")
    if args.type in ("subscription", "trial") and not args.duration:
        parser.error(f"--duration is required for {args.type} licenses")

    return cli_mode(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n  Cancelled by user.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
