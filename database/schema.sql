CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT,
    description TEXT,
    tags TEXT,
    location TEXT,
    source TEXT,
    url TEXT,
    posted_at TEXT,
    collected_at TEXT NOT NULL,
    experience_level TEXT,
    score INTEGER,
    posted_to_discord INTEGER DEFAULT 0,
    posted_to_telegram INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_jobs_source ON jobs(source);
CREATE INDEX IF NOT EXISTS idx_jobs_collected_at ON jobs(collected_at);
CREATE INDEX IF NOT EXISTS idx_jobs_score ON jobs(score);
