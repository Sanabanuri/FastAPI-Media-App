import requests
import os

BASE_URL = "http://127.0.0.1:8000"

def get_token():
    # Helper to get a valid token
    email = "testuser_success@example.com"
    password = "correctpassword"
    
    # Ensure user exists (idempotent registry)
    requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password, "is_active": True, "is_superuser": False, "is_verified": True})
    
    response = requests.post(f"{BASE_URL}/auth/jwt/login", data={"username": email, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    raise Exception(f"Failed to get token: {response.text}")

def test_upload(token):
    print("\nTesting /upload endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a dummy image file
    with open("test_image.txt", "w") as f:
        f.write("This is a dummy image file content.")
    
    try:
        files = {"file": ("test_image.txt", open("test_image.txt", "rb"), "text/plain")}
        data = {"caption": "Test caption"}
        
        response = requests.post(f"{BASE_URL}/upload", files=files, data=data, headers=headers)
        
        if response.status_code == 200:
            print("PASS: Upload successful.")
            return response.json()
        else:
            print(f"FAIL: Upload failed. Status: {response.status_code}, Body: {response.text}")
    finally:
        if os.path.exists("test_image.txt"):
            os.remove("test_image.txt")

def test_feed(token):
    print("\nTesting /feed endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/feed", headers=headers)
    
    if response.status_code == 200:
        print("PASS: Feed fetched successfully.")
        print(f"Feed content: {response.json()}")
    else:
        print(f"FAIL: Feed failed. Status: {response.status_code}, Body: {response.text}")

if __name__ == "__main__":
    try:
        token = get_token()
        print(f"Token acquired. Testing endpoints...")
        test_upload(token)
        test_feed(token)
    except Exception as e:
        print(f"Error: {e}")
