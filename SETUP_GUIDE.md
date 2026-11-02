# Database Setup Guide

## Execute These SQL Files One by One in Supabase

### Step 1: Create Users Table
1. Open `step1_users_table.sql`
2. Copy the content
3. Paste in Supabase SQL Editor
4. Click "Run"
5. Wait for "Success" message

### Step 2: Create Chat History Table
1. Open `step2_chat_history_table.sql`
2. Copy the content
3. Paste in Supabase SQL Editor
4. Click "Run"
5. Wait for "Success" message

### Step 3: Create Document Embeddings Table (Simplified)
1. Open `step3_document_embeddings_simple.sql`
2. Copy the content
3. Paste in Supabase SQL Editor
4. Click "Run"
5. Wait for "Success" message

### Step 4: Add Security Policies
1. Open `step4_security_policies.sql`
2. Copy the content
3. Paste in Supabase SQL Editor
4. Click "Run"
5. Wait for "Success" message

## After All Steps Complete:

Run this test:
```bash
python test_connection_simple.py
```

You should see:
```
Testing basic Supabase connection...
Supabase URL: https://wxeqyvhwjlcwinappjwt.supabase.co
Success! Users table exists and is accessible.
```

## Then Create Embeddings:

1. Make sure you have OPENAI_API_KEY in your .env file
2. Run: `python create_embeddings.py`

## Troubleshooting:

If you still get schema cache errors:
1. Go to Project Settings > API
2. Click "Reset schema cache"
3. Wait 1-2 minutes
4. Run the test again
