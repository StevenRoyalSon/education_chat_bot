"""
Test with direct insert - this will force the schema to refresh
"""

from database import supabase

print("Testing by inserting a test user...")

try:
    # Try to insert a test user
    result = supabase.table("users").insert({
        "name": "Test User",
        "email": "test@example.com",
        "password": "test123"
    }).execute()
    
    print("Success! Test user created.")
    print(f"User ID: {result.data[0]['id']}")
    
    # Now try to read it back
    result2 = supabase.table("users").select("*").execute()
    print(f"Total users in database: {len(result2.data)}")
    
except Exception as e:
    error_msg = str(e)
    print(f"Error: {error_msg}")
    
    if "Could not find the table" in error_msg:
        print("\nSchema cache issue detected.")
        print("Please try:")
        print("1. Go to Project Settings > API")
        print("2. Click 'Reset schema cache' or 'Restart API'")
        print("3. Wait 1-2 minutes")
        print("4. Run this test again")
