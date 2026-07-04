"""Test settings API endpoint."""
import requests
import json

# Step 1: Login
print("[1] Logging in...")
login_response = requests.post(
    "http://127.0.0.1:8000/auth/login",
    data={"username": "admin", "password": "admin123"},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

if login_response.status_code != 200:
    print(f"[FAIL] Login failed: {login_response.status_code}")
    print(login_response.text)
    exit(1)

token = login_response.json()["access_token"]
print(f"[OK] Got token: {token[:50]}...")

# Step 2: Test settings endpoint
print("\n[2] Fetching settings...")
settings_response = requests.get(
    "http://127.0.0.1:8000/settings/",
    headers={"Authorization": f"Bearer {token}"}
)

print(f"Status: {settings_response.status_code}")
print(f"Response: {json.dumps(settings_response.json(), indent=2)}")

if settings_response.status_code == 200:
    print("\n[SUCCESS] Settings endpoint works!")
else:
    print(f"\n[FAIL] Settings endpoint returned {settings_response.status_code}")
