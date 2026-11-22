-- Create subscriptions table in Supabase
-- Run this SQL in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS subscriptions (
    id BIGSERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    source TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(email, source)
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_subscriptions_email ON subscriptions(email);
CREATE INDEX IF NOT EXISTS idx_subscriptions_source ON subscriptions(source);
CREATE INDEX IF NOT EXISTS idx_subscriptions_email_source ON subscriptions(email, source);

-- Enable Row Level Security (RLS)
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- Security Note:
-- If using Supabase Auth, ensure users only access their own subscriptions:
-- CREATE POLICY "Users can view own subscriptions" ON subscriptions
--     FOR SELECT USING (auth.jwt() ->> 'email' = email);
--
-- CREATE POLICY "Users can insert own subscriptions" ON subscriptions
--     FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = email);
--
-- CREATE POLICY "Users can delete own subscriptions" ON subscriptions
--     FOR DELETE USING (auth.jwt() ->> 'email' = email);

-- Service role bypasses RLS automatically for backend scrapers and workers.
