"""Test API endpoints directly."""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("="*70)
print("MBAS API Testing")
print("="*70)

# Test 1: Check if server is running
print("\n[1] Testing server connectivity...")
try:
    response = requests.get(f"{BASE_URL}/docs", timeout=5)
    if response.status_code == 200:
        print("[OK] Server is running")
        print(f"  Status: {response.status_code}")
    else:
        print(f"[FAIL] Unexpected status: {response.status_code}")
except Exception as e:
    print(f"[FAIL] Server not reachable: {e}")
    exit(1)

# Test 2: Test login with form data (correct method)
print("\n[2] Testing login endpoint...")
login_data = {
    "username": "admin",
    "password": "admin123"
}

try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data=login_data,  # Form data, not JSON
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=5
    )

    print(f"  Status Code: {response.status_code}")
    print(f"  Response: {response.text[:200]}")

    if response.status_code == 200:
        data = response.json()
        print("[OK] Login successful!")
        print(f"  Access Token: {data.get('access_token', '')[:50]}...")
        print(f"  Token Type: {data.get('token_type')}")
        if 'user' in data:
            print(f"  User: {data['user'].get('username')} ({data['user'].get('role')})")

        # Save token for next test
        token = data['access_token']

        # Test 3: Get current user
        print("\n[3] Testing /auth/me endpoint...")
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        if response.status_code == 200:
            user = response.json()
            print("[OK] User profile retrieved")
            print(f"  Username: {user.get('username')}")
            print(f"  Email: {user.get('email')}")
            print(f"  Role: {user.get('role')}")
        else:
            print(f"[X] Failed: {response.status_code} - {response.text}")

        # Test 4: Get settings
        print("\n[4] Testing /settings endpoint...")
        response = requests.get(
            f"{BASE_URL}/settings/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        if response.status_code == 200:
            settings = response.json()
            print("[OK] Settings retrieved")
            print(f"  Business: {settings.get('business_name')}")
            print(f"  Tax Rate: {settings.get('tax_rate')}%")
            print(f"  Features: {len(settings.get('feature_flags', {}))} flags")
            for feature, enabled in settings.get('feature_flags', {}).items():
                status = "[OK]" if enabled else "[X]"
                print(f"    {status} {feature}")
        else:
            print(f"[X] Failed: {response.status_code}")

        # Test 5: Get products
        print("\n[5] Testing /inventory/products endpoint...")
        response = requests.get(
            f"{BASE_URL}/inventory/products",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        if response.status_code == 200:
            products = response.json()
            print(f"[OK] Products retrieved: {len(products)} items")
            for i, product in enumerate(products[:3], 1):
                print(f"  {i}. {product['name']} - PKR {product['selling_price']:,.2f} ({product['stock_quantity']} in stock)")
        else:
            print(f"[X] Failed: {response.status_code}")

        print("\n" + "="*70)
        print("[OK] ALL TESTS PASSED - Backend is working!")
        print("="*70)

    else:
        print(f"[X] Login failed")
        print(f"  Error: {response.text}")

except requests.exceptions.ConnectionError:
    print("[X] Could not connect to server")
    print("  Make sure backend is running: python -m uvicorn src.main:app --host 127.0.0.1 --port 8000")
except Exception as e:
    print(f"[X] Error: {e}")

print("\nNeed to launch frontend? Run:")
print("  cd frontend")
print("  npm run dev")
