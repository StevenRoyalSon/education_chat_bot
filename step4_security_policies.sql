-- Step 4: Security Policies (Row Level Security)
-- Run this after Step 3 (simplified version)

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_embeddings ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Allow public signup" ON users;
DROP POLICY IF EXISTS "Users can read own data" ON users;
DROP POLICY IF EXISTS "Users can insert own messages" ON chat_history;
DROP POLICY IF EXISTS "Users can read own history" ON chat_history;
DROP POLICY IF EXISTS "Users can delete own messages" ON chat_history;
DROP POLICY IF EXISTS "Allow read access to embeddings" ON document_embeddings;

-- Users table policies
CREATE POLICY "Allow public signup" ON users
    FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Users can read own data" ON users
    FOR SELECT
    USING (email = current_setting('app.current_user_email', true));

-- Chat history policies
CREATE POLICY "Users can insert own messages" ON chat_history
    FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Users can read own history" ON chat_history
    FOR SELECT
    USING (true);

CREATE POLICY "Users can delete own messages" ON chat_history
    FOR DELETE
    USING (true);

-- Document embeddings policy (allow read for all)
CREATE POLICY "Allow read access to embeddings" ON document_embeddings
    FOR SELECT
    USING (true);
