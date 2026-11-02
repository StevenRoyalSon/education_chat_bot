"""
Simple connection test - just checks if we can connect to Supabase
"""

from database import supabase, SUPABASE_URL

print("Testing basic Supabase connection...")
print(f"Supabase URL: {SUPABASE_URL}")

try:
    # Try to get the current schema information
    # This should work even if tables don't exist
    response = supabase.table("users").select("*").execute()
    print("Success! Users table exists and is accessible.")
except Exception as e:
    error_msg = str(e)
    print(f"Error: {error_msg}")

    if "Could not find the table" in error_msg:
        print("\nThe users table does not exist yet.")
        print("Please check:")
        print("1. Did the SQL execute successfully in Supabase?")
        print("2. Check the Table Editor to see if 'users' table is listed")
        print("3. Try running this SQL in SQL Editor:")
        print("   SELECT * FROM information_schema.tables WHERE table_name = 'users';")
    else:
        print(f"\nConnection failed with error: {error_msg}")
