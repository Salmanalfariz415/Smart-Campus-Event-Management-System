"""
Test Flask API endpoints to verify the app is working
"""
import requests
import json
import time

def test_api_endpoints():
    base_url = "http://127.0.0.1:5000"
    print("=== TESTING FLASK API ENDPOINTS ===\n")
    
    # Wait a moment for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    try:
        print("1. Testing registration endpoint...")
        register_data = {
            "username": "testuser2@example.com",
            "password": "testpass123"
        }
        
        response = requests.post(f"{base_url}/auth/register", json=register_data, timeout=10)
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Registration successful! User ID: {result.get('user_id')}")
            user_token = result.get('token')
        else:
            print(f"Registration response: {response.status_code} - {response.text}")
            user_token = None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server. Make sure it's running on port 5000.")
        return False
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
        user_token = None
        
    try:
        print("\n2. Testing login endpoint...")
        login_data = {
            "username": "testuser2@example.com", 
            "password": "testpass123"
        }
        
        response = requests.post(f"{base_url}/auth/login", json=login_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Login successful! Token received.")
        else:
            print(f"Login response: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        
    print("\n3. Testing organizer registration...")
    try:
        organizer_data = {
            "org_name": "Test Organization",
            "org_type": "Student Club", 
            "contact_name": "Test Contact",
            "contact_position": "President",
            "email": "testorg@example.com",
            "phone": "1234567890",
            "password": "testpass123",
            "confirm_password": "testpass123",
            "org_description": "A test organization"
        }
        
        response = requests.post(f"{base_url}/auth/register_organizer", json=organizer_data, timeout=10)
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Organizer registration successful! User ID: {result.get('user_id')}")
        else:
            print(f"Organizer registration response: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Organizer registration test failed: {e}")
        
    return True

if __name__ == "__main__":
    test_api_endpoints()