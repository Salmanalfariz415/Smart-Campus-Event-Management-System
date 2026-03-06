"""
Test Supabase Connection

This script tests if your Supabase connection is working properly.
Run this after setting up your .env file with Supabase credentials.
"""
import os
from dotenv import load_dotenv
from app.db.sql_connection import get_sql_connection, get_supabase_client

def test_postgresql_connection():
    """Test direct PostgreSQL connection to Supabase"""
    print("Testing PostgreSQL connection...")
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        print(f"✅ PostgreSQL connection successful!")
        print(f"Database version: {version[0]}")
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def test_supabase_client():
    """Test Supabase Python client"""
    print("\nTesting Supabase client...")
    try:
        supabase = get_supabase_client()
        # Try a simple query to test connection
        result = supabase.table('users').select('count', count='exact').execute()
        print(f"✅ Supabase client connection successful!")
        print(f"Users table accessible (count query worked)")
        return True
    except Exception as e:
        print(f"❌ Supabase client connection failed: {e}")
        return False

def test_environment_variables():
    """Check if all required environment variables are set"""
    print("\nChecking environment variables...")
    load_dotenv()
    
    required_vars = {
        'SUPABASE_URL': os.getenv('SUPABASE_URL'),
        'SUPABASE_SERVICE_ROLE_KEY': os.getenv('SUPABASE_SERVICE_ROLE_KEY'),
        'SUPABASE_DATABASE_URL': os.getenv('SUPABASE_DATABASE_URL'),
        'SECRET_KEY': os.getenv('SECRET_KEY')
    }
    
    all_set = True
    for var_name, var_value in required_vars.items():
        if var_value:
            print(f"✅ {var_name}: Set")
        else:
            print(f"❌ {var_name}: Not set")
            all_set = False
    
    return all_set

if __name__ == "__main__":
    print("=== SUPABASE CONNECTION TEST ===\n")
    
    # Test environment variables
    if not test_environment_variables():
        print("\n❌ Please set up your .env file with Supabase credentials first!")
        print("Copy .env.example to .env and fill in your credentials.")
        exit(1)
    
    # Test PostgreSQL connection
    postgresql_success = test_postgresql_connection()
    
    # Test Supabase client
    supabase_success = test_supabase_client()
    
    print("\n=== SUMMARY ===")
    if postgresql_success and supabase_success:
        print("🎉 All connections successful! Your app is ready to use Supabase.")
    else:
        print("⚠️  Some connections failed. Check your configuration.")
        if not postgresql_success:
            print("   - Check SUPABASE_DATABASE_URL in your .env file")
        if not supabase_success:
            print("   - Check SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in your .env file")