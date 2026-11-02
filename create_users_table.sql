-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add comments
COMMENT ON TABLE users IS 'Stores user registration details for the education chatbot';
COMMENT ON COLUMN users.id IS 'Unique identifier for each user';
COMMENT ON COLUMN users.name IS 'Full name of the user';
COMMENT ON COLUMN users.email IS 'User email address (must be unique)';
COMMENT ON COLUMN users.password IS 'Hashed password for authentication';
COMMENT ON COLUMN users.created_at IS 'Timestamp when user was created';

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Allow anyone to insert new users (for signup)
CREATE POLICY "Allow public signup" ON users
    FOR INSERT
    WITH CHECK (true);

-- Allow users to read their own data based on email
CREATE POLICY "Users can read own data" ON users
    FOR SELECT
    USING (email = current_setting('app.current_user_email', true));

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
