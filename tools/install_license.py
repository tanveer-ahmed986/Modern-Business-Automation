#!/usr/bin/env python3
"""
MBAS License Installation Tool

Installs license file to the correct system location for production use.
Requires administrator privileges for system-wide installation.
"""

import sys
import shutil
import argparse
from pathlib import Path


def is_admin():
    """Check if running with administrator privileges (Windows)."""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        # On non-Windows or if check fails, assume not admin
        return False


def get_installation_paths():
    """Get available license installation paths."""
    paths = {
        "system": Path("C:/ProgramData/MBAS"),
        "user": Path.home() / "AppData/Local/MBAS",
        "current": Path.cwd()
    }
    return paths


def install_license(source_path: Path, location: str = "system") -> bool:
    """
    Install license file to specified location.

    Args:
        source_path: Path to source .mbas-license file
        location: Installation location (system, user, or current)

    Returns:
        True if successful, False otherwise
    """
    # Validate source file
    if not source_path.exists():
        print(f"[ERROR] Source license file not found: {source_path}")
        return False

    if not source_path.suffix == ".mbas-license":
        print(f"[WARNING] File extension is not .mbas-license: {source_path}")
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response != 'y':
            return False

    # Get target directory
    paths = get_installation_paths()
    if location not in paths:
        print(f"[ERROR] Invalid location: {location}")
        print(f"Valid locations: {', '.join(paths.keys())}")
        return False

    target_dir = paths[location]
    target_file = target_dir / "mbas.license"

    # Check admin privileges for system install
    if location == "system" and not is_admin():
        print("[ERROR] System-wide installation requires administrator privileges")
        print("Please run this script as administrator (right-click -> Run as administrator)")
        return False

    # Create target directory
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Created directory: {target_dir}")
    except PermissionError:
        print(f"[ERROR] Permission denied creating directory: {target_dir}")
        print("Try running as administrator or choose 'user' location")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to create directory: {e}")
        return False

    # Copy license file
    try:
        shutil.copy2(source_path, target_file)
        print(f"[OK] License installed to: {target_file}")

        # Verify installation
        if target_file.exists():
            file_size = target_file.stat().st_size
            print(f"[OK] Verified: {file_size} bytes")
            return True
        else:
            print("[ERROR] License file not found after copy")
            return False

    except PermissionError:
        print(f"[ERROR] Permission denied writing to: {target_file}")
        print("Try running as administrator or choose 'user' location")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to copy license: {e}")
        return False


def verify_license(license_path: Path):
    """
    Verify license file integrity.

    Args:
        license_path: Path to license file to verify
    """
    print("\n" + "=" * 70)
    print("  License Verification")
    print("=" * 70)

    if not license_path.exists():
        print(f"[ERROR] License file not found: {license_path}")
        return

    try:
        import json

        with open(license_path, 'r') as f:
            license_data = json.load(f)

        # Display license info
        print(f"\nLicensee:     {license_data.get('licensee', 'N/A')}")
        print(f"Tier:         {license_data.get('tier', 'N/A').upper()}")
        print(f"Issued:       {license_data.get('issued_date', 'N/A')}")
        print(f"Expires:      {license_data.get('expiry_date', 'NEVER (Perpetual)')}")
        print(f"Machine Lock: {'YES' if license_data.get('machine_id_hash') else 'NO'}")

        # Verify signature exists
        if 'signature' in license_data and license_data['signature']:
            print(f"\n[OK] License signature present ({len(license_data['signature'])} chars)")
        else:
            print("\n[ERROR] License signature missing!")

        # List features
        features = license_data.get('features', {})
        if features:
            print("\nEnabled Features:")
            for feature, enabled in sorted(features.items()):
                status = "[YES]" if enabled else "[ NO]"
                print(f"  {status} {feature}")

    except json.JSONDecodeError:
        print("[ERROR] Invalid JSON format")
    except Exception as e:
        print(f"[ERROR] Failed to read license: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Install MBAS license file to system location",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Installation Locations:
  system  - C:\\ProgramData\\MBAS\\mbas.license (requires admin)
  user    - %USERPROFILE%\\AppData\\Local\\MBAS\\mbas.license
  current - Current directory (for development)

Examples:
  # Install to system directory (recommended for production)
  python install_license.py customer.mbas-license --location system

  # Install to user directory (no admin required)
  python install_license.py customer.mbas-license --location user

  # Verify license without installing
  python install_license.py customer.mbas-license --verify-only
        """
    )

    parser.add_argument(
        'license_file',
        type=Path,
        help='Path to .mbas-license file to install'
    )

    parser.add_argument(
        '--location',
        choices=['system', 'user', 'current'],
        default='system',
        help='Installation location (default: system)'
    )

    parser.add_argument(
        '--verify-only',
        action='store_true',
        help='Verify license without installing'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("  MBAS License Installation Tool")
    print("=" * 70)
    print()

    # Verify license
    verify_license(args.license_file)

    # Install if requested
    if not args.verify_only:
        print("\n" + "=" * 70)
        print(f"  Installing to: {args.location}")
        print("=" * 70)
        print()

        success = install_license(args.license_file, args.location)

        if success:
            print("\n" + "=" * 70)
            print("  INSTALLATION SUCCESSFUL!")
            print("=" * 70)
            print("\nNext steps:")
            print("  1. Restart MBAS application")
            print("  2. Verify features are enabled in Settings")
            print("  3. Test licensed functionality")
            print()
        else:
            print("\n" + "=" * 70)
            print("  INSTALLATION FAILED")
            print("=" * 70)
            print("\nTroubleshooting:")
            print("  - Ensure you have a valid .mbas-license file")
            print("  - For system install, run as administrator")
            print("  - Try --location user if admin access unavailable")
            print()
            sys.exit(1)
    else:
        print("\n[INFO] Verification only mode - license not installed")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Installation cancelled by user")
        sys.exit(1)
