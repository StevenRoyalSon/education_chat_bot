"""
Test Database Connection
Run this to verify your Supabase connection is working
"""

from database import supabase, SUPABASE_URL

# Test the connection
print("Testing Supabase connection...")
print(f"Supabase URL: {SUPABASE_URL}")

try:
    # Try to query the users table
    result = supabase.table("users").select("count").execute()
    print("✓ Database connection successful!")
    print(f"✓ Users table exists and is accessible")
except Exception as e:
    print(f"✗ Database connection failed: {e}")
    print("\nPlease check:")
    print("1. Your .env file has correct SUPABASE_URL and SUPABASE_KEY")
    print("2. You have executed the database.sql file in Supabase")
    print("3. Your Supabase project is active")
