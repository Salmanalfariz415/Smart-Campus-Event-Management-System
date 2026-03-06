"""
Supabase Table Setup Script

This script contains the SQL commands to create the necessary tables in your Supabase database.
You can run these commands in the Supabase SQL editor.
"""

# Create users table
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Create organizers table
CREATE_ORGANIZERS_TABLE = """
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
"""

# Create events table 
CREATE_EVENTS_TABLE = """
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
"""

# Create bookings table
CREATE_BOOKINGS_TABLE = """
CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    booking_status VARCHAR(50) DEFAULT 'confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, event_id)
);
"""

# Enable Row Level Security (optional but recommended)
ENABLE_RLS = """
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE organizers ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;
"""

def print_setup_instructions():
    """Print setup instructions for Supabase"""
    print("=== SUPABASE SETUP INSTRUCTIONS ===")
    print("1. Go to your Supabase project dashboard")
    print("2. Navigate to the SQL Editor")
    print("3. Run the following SQL commands in order:")
    print("\n--- Users Table ---")
    print(CREATE_USERS_TABLE)
    print("\n--- Organizers Table ---")
    print(CREATE_ORGANIZERS_TABLE)
    print("\n--- Events Table ---")
    print(CREATE_EVENTS_TABLE)
    print("\n--- Bookings Table ---")
    print(CREATE_BOOKINGS_TABLE)
    print("\n--- Enable Row Level Security (Optional) ---")
    print(ENABLE_RLS)
    print("\n=== ENVIRONMENT SETUP ===")
    print("4. Copy .env.example to .env")
    print("5. Fill in your Supabase credentials in .env")
    print("6. Your app should now connect to Supabase!")

if __name__ == "__main__":
    print_setup_instructions()