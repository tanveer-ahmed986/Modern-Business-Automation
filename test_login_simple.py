"""Simple login test with error details."""
import requests

url = "http://127.0.0.1:8000/auth/login"
data = {"username": "admin", "password": "admin123"}

print("Testing login...")
try:
    response = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        print("\n[SUCCESS] Authentication works!")
        data = response.json()
        print(f"Token: {data.get('access_token', '')[:50]}...")
    else:
        print(f"\n[FAIL] Status {response.status_code}")

except Exception as e:
    print(f"Error: {e}")
