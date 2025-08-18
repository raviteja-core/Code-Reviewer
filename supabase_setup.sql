-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(64),
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(512) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create code_submissions table
CREATE TABLE IF NOT EXISTS code_submissions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    code_text TEXT NOT NULL,
    language VARCHAR(20),
    detected_language VARCHAR(20),
    feedback TEXT,
    ai_score INTEGER,
    comments TEXT,
    plagiarism_hints TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_submissions_user_id ON code_submissions(user_id);
CREATE INDEX IF NOT EXISTS idx_submissions_timestamp ON code_submissions(timestamp DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE code_submissions ENABLE ROW LEVEL SECURITY;

-- Create policies for users table
CREATE POLICY "Users can view their own data" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can insert their own data" ON users
    FOR INSERT WITH CHECK (true);

-- Create policies for code_submissions table
CREATE POLICY "Users can view their own submissions" ON code_submissions
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own submissions" ON code_submissions
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own submissions" ON code_submissions
    FOR UPDATE USING (auth.uid()::text = user_id::text);

-- Note: For this application, we're using email-based authentication instead of Supabase Auth
-- So we'll need to disable RLS or create custom policies based on email matching
-- For now, let's disable RLS to allow the application to work with email-based auth

ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE code_submissions DISABLE ROW LEVEL SECURITY; 