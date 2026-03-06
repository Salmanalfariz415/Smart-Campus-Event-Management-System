"""
Quick test of Supabase authentication functions
"""
import sys
sys.path.append('.')

from app.dao.auth_dao_supabase import register_user_supabase, login_user_supabase
import traceback

def test_auth_functions():
    print("=== TESTING SUPABASE AUTH FUNCTIONS ===\n")
    
    test_email = "test@example.com"
    test_password = "testpassword123"
    
    try:
        print("1. Testing user registration...")
        result = register_user_supabase(test_email, test_password)
        print(f"✅ Registration successful! User ID: {result['user_id']}")
        print(f"✅ Token generated: {result['token'][:50]}...")
        
        print("\n2. Testing user login...")
        login_result = login_user_supabase(test_email, test_password)
        if login_result == "Incorrect username or password":
            print("❌ Login failed")
        else:
            print(f"✅ Login successful! Token: {login_result[:50]}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_auth_functions()