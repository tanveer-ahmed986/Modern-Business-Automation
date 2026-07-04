"""Check database contents."""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.security import verify_password

db = sqlite3.connect("mbas.db")
cursor = db.cursor()

# Check users
print("=== USERS ===")
cursor.execute("SELECT id, username, email, role, hashed_password FROM user")
users = cursor.fetchall()
for user in users:
    print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")
    print(f"  Hash: {user[4][:60]}...")

    # Test password verification
    if user[1] == "admin":
        test_password = "admin123"
        is_valid = verify_password(test_password, user[4])
        print(f"  Password '{test_password}' valid: {is_valid}")

print("\n=== PRODUCTS ===")
cursor.execute("SELECT COUNT(*) FROM product")
print(f"Total products: {cursor.fetchone()[0]}")

print("\n=== SETTINGS ===")
cursor.execute("SELECT id, business_name, tax_rate, currency_symbol FROM settings")
settings = cursor.fetchone()
if settings:
    print(f"Business: {settings[1]}")
    print(f"Tax Rate: {settings[2]}%")
    print(f"Currency: {settings[3]}")

db.close()
