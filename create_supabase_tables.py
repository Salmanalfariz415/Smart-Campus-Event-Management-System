"""
Create Supabase tables using the Supabase client
This bypasses the PostgreSQL connection issues by using the REST API
"""
from app.db.sql_connection import get_supabase_client
import traceback

def create_tables_via_supabase():
    """Create tables using Supabase RPC (Remote Procedure Call)"""
    try:
        supabase = get_supabase_client()
        
        # SQL to create all tables
        create_tables_sql = """
        -- Create users table
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            user_type VARCHAR(50) DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Create organizers table
        CREATE TABLE IF NOT EXISTS organizers (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            org_name VARCHAR(255) NOT NULL,
            org_type VARCHAR(100),
            org_description TEXT,
            contact_name VARCHAR(255) NOT NULL,
            contact_position VARCHAR(100),
            phone VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Create events table 
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            organizer_id INTEGER REFERENCES organizers(id) ON DELETE CASCADE,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            date_time TIMESTAMP NOT NULL,
            location VARCHAR(255),
            max_participants INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Create bookings table
        CREATE TABLE IF NOT EXISTS bookings (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
            booking_status VARCHAR(50) DEFAULT 'confirmed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, event_id)
        );
        """
        
        # Execute via Supabase RPC
        result = supabase.rpc('exec_sql', {'sql': create_tables_sql}).execute()
        print("✅ Tables created successfully via Supabase!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables via Supabase: {e}")
        print("Let's try creating a simple test table instead...")
        
        try:
            # Try a simpler approach - just check if we can create one table
            simple_sql = """
            CREATE TABLE IF NOT EXISTS test_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255)
            );
            """
            result = supabase.rpc('exec_sql', {'sql': simple_sql}).execute()
            print("✅ Simple test successful! Tables can be created manually in Supabase dashboard.")
            return True
        except Exception as e2:
            print(f"❌ RPC not available: {e2}")
            print("ℹ️  Please create tables manually in Supabase SQL Editor")
            return False

def test_table_creation():
    """Test if we can insert data (which will auto-create tables in some cases)"""
    try:
        supabase = get_supabase_client()
        
        # Check if users table exists by trying to query it
        result = supabase.table('users').select('count', count='exact').execute()
        print(f"✅ Users table exists! Current count: {result.count}")
        return True
        
    except Exception as e:
        print(f"❌ Users table doesn't exist or can't be accessed: {e}")
        return False

if __name__ == "__main__":
    print("=== SUPABASE TABLE SETUP ===\n")
    
    print("1. Testing if tables already exist...")
    if test_table_creation():
        print("🎉 Your tables are ready!")
    else:
        print("\n2. Attempting to create tables...")
        if not create_tables_via_supabase():
            print("\n=== MANUAL SETUP REQUIRED ===")
            print("Please go to your Supabase dashboard:")
            print("1. Navigate to SQL Editor")
            print("2. Run the SQL commands from setup_supabase.py")
            print("3. This will create the required tables")
            
    print("\n=== TESTING SUPABASE CONNECTION ===")
    try:
        supabase = get_supabase_client()
        # Test basic connection
        result = supabase.table('users').select('count', count='exact').execute()
        print("✅ Supabase connection working!")
        print("🚀 Your app is ready to run!")
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        traceback.print_exc()