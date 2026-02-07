import requests

BASE_URL = "http://127.0.0.1:8000"

def test_login_unregistered_user():
    print("Testing login for unregistered user...")
    response = requests.post(f"{BASE_URL}/auth/jwt/login", data={"username": "nonexistent@example.com", "password": "password123"})
    if response.status_code == 400:
        try:
            detail = response.json().get("detail")
            if detail == "User not registered":
                print("PASS: Correctly identified unregistered user.")
            else:
                print(f"FAIL: Expected 'User not registered', got '{detail}'")
        except:
             print(f"FAIL: Could not parse JSON response. Body: {response.text}")
    else:
        print(f"FAIL: Expected status code 400, got {response.status_code}. Body: {response.text}")

def test_login_invalid_credentials():
    print("\nTesting login for registered user with wrong password...")
    # First ensure a user exists (or use a known one if possible, but for now we'll rely on one being there or create one if needed)
    # For this test to work reliably, we need a known user. I'll try to register one first just in case.
    email = "testuser@example.com"
    password = "correctpassword"
    
    requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password, "is_active": True, "is_superuser": False, "is_verified": True})

    response = requests.post(f"{BASE_URL}/auth/jwt/login", data={"username": email, "password": "wrongpassword"})
    if response.status_code == 400:
        try:
            detail = response.json().get("detail")
            if detail == "Invalid credentials": # Or whatever standard message fastapi-users gives or we customized
                print("PASS: Correctly identified invalid credentials.")
            elif detail == "LOGIN_BAD_CREDENTIALS": # The code in user.py uses this for inactive/unverified users, but for bad password it might be different depending on backend
                 print(f"FAIL: Got 'LOGIN_BAD_CREDENTIALS', expected 'Invalid credentials' or similar.")
            else:
                 print(f"FAIL: Expected 'Invalid credentials', got '{detail}'")
        except:
             print(f"FAIL: Could not parse JSON response. Body: {response.text}")
    else:
        print(f"FAIL: Expected status code 400, got {response.status_code}. Body: {response.text}")

def test_login_success():
    print("\nTesting login for registered user with CORRECT password...")
    email = "testuser_success@example.com"
    password = "correctpassword"
    
    # Register
    requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password, "is_active": True, "is_superuser": False, "is_verified": True})

    # Login
    response = requests.post(f"{BASE_URL}/auth/jwt/login", data={"username": email, "password": password})
    if response.status_code == 200:
        if "access_token" in response.json():
             print("PASS: Login successful (unverified userAllowed).")
        else:
             print(f"FAIL: Status 200 but no token? Body: {response.text}")
    else:
        print(f"FAIL: Expected status code 200, got {response.status_code}. Body: {response.text}")

if __name__ == "__main__":
    test_login_unregistered_user()
    test_login_invalid_credentials()
    test_login_success()
