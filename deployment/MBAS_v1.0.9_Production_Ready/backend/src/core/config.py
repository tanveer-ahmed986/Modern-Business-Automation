"""
Dynamic configuration management for MBAS backend.

Handles SECRET_KEY generation and storage for JWT token signing.
"""

import secrets
from pathlib import Path


# Configuration directory (will be created if it doesn't exist)
CONFIG_DIR = Path("config")
SECRET_KEY_FILE = CONFIG_DIR / "secret.key"


def get_or_create_secret_key() -> str:
    """
    Generate unique SECRET_KEY on first run, load on subsequent runs.

    The SECRET_KEY is used for JWT token signing and must be:
    - Unique per installation
    - Persistent across restarts
    - Never hardcoded in source code

    Returns:
        str: The SECRET_KEY (64-byte URL-safe base64 string)
    """
    # Create config directory if it doesn't exist
    CONFIG_DIR.mkdir(exist_ok=True)

    # Load existing key if available
    if SECRET_KEY_FILE.exists():
        try:
            return SECRET_KEY_FILE.read_text().strip()
        except Exception as e:
            print(f"[!] Warning: Failed to read existing SECRET_KEY: {e}")
            print("[!] Generating new SECRET_KEY...")

    # Generate new key
    secret_key = secrets.token_urlsafe(64)

    # Save to file
    try:
        SECRET_KEY_FILE.write_text(secret_key)

        # Set restrictive permissions (owner read/write only)
        # Note: chmod may not work on Windows, but we try anyway
        try:
            SECRET_KEY_FILE.chmod(0o600)
        except Exception:
            pass  # Windows doesn't support Unix permissions

        print(f"[OK] Generated new SECRET_KEY at {SECRET_KEY_FILE}")
        print("[!] Keep this file secret and backed up!")

    except Exception as e:
        print(f"[!] Failed to save SECRET_KEY to file: {e}")
        print("[!] Using in-memory key (will not persist across restarts)")

    return secret_key


# Export the SECRET_KEY for use in auth module
SECRET_KEY = get_or_create_secret_key()
