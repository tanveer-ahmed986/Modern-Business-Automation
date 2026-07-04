"""Diagnose authentication issue."""
import sys
from pathlib import Path
import traceback

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("="*70)
print("AUTHENTICATION DIAGNOSTICS")
print("="*70)

# Test 1: Import core modules
print("\n[1] Testing core imports...")
try:
    from core.config import SECRET_KEY
    print(f"[OK] SECRET_KEY imported: {SECRET_KEY[:20]}...")
except Exception as e:
    print(f"[FAIL] SECRET_KEY import failed: {e}")
    traceback.print_exc()

try:
    from core.auth import create_access_token
    print("[OK] create_access_token imported")
except Exception as e:
    print(f"[FAIL] create_access_token import failed: {e}")
    traceback.print_exc()

try:
    from core.security import verify_password, get_password_hash
    print("[OK] Security functions imported")
except Exception as e:
    print(f"[FAIL] Security import failed: {e}")
    traceback.print_exc()

# Test 2: Database connection
print("\n[2] Testing database connection...")
try:
    from core.db import engine, get_session
    from sqlmodel import Session, select
    from models.core import User

    with Session(engine) as session:
        users = session.exec(select(User)).all()
        print(f"[OK] Database connected: {len(users)} users found")

        admin = session.exec(select(User).where(User.username == "admin")).first()
        if admin:
            print(f"[OK] Admin user exists: {admin.username}")
            print(f"     Hash: {admin.hashed_password[:50]}...")
        else:
            print("[FAIL] Admin user not found")

except Exception as e:
    print(f"[FAIL] Database error: {e}")
    traceback.print_exc()

# Test 3: Password verification
print("\n[3] Testing password verification...")
try:
    if admin:
        from core.security import verify_password
        is_valid = verify_password("admin123", admin.hashed_password)
        print(f"[OK] Password verification test: {is_valid}")
        if not is_valid:
            print("[!] WARNING: Password does not match!")
except Exception as e:
    print(f"[FAIL] Password verification error: {e}")
    traceback.print_exc()

# Test 4: JWT token creation
print("\n[4] Testing JWT token creation...")
try:
    from core.auth import create_access_token
    token = create_access_token(subject="admin")
    print(f"[OK] JWT token created: {token[:50]}...")
except Exception as e:
    print(f"[FAIL] JWT creation error: {e}")
    traceback.print_exc()

# Test 5: Simulate login flow
print("\n[5] Testing complete login flow...")
try:
    from fastapi.security import OAuth2PasswordRequestForm
    from core.db import get_session
    from core.auth import create_access_token
    from core.security import verify_password
    from models.core import User
    from sqlmodel import Session, select

    with Session(engine) as session:
        # Simulate form data
        username = "admin"
        password = "admin123"

        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()

        if not user:
            print(f"[FAIL] User '{username}' not found")
        else:
            print(f"[OK] User found: {user.username}")

            if not verify_password(password, user.hashed_password):
                print(f"[FAIL] Password verification failed")
            else:
                print(f"[OK] Password verified")

                token = create_access_token(subject=user.username)
                print(f"[OK] Token created: {token[:50]}...")
                print("\n[SUCCESS] Complete login flow works!")

except Exception as e:
    print(f"[FAIL] Login flow error: {e}")
    traceback.print_exc()

print("\n" + "="*70)
print("DIAGNOSTICS COMPLETE")
print("="*70)
