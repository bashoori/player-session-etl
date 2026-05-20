-- Raw-level “staging” (optional for learning)
CREATE TABLE IF NOT EXISTS staging_player_sessions (
    player_id TEXT NOT NULL,
    game_id   TEXT NOT NULL,
    session_start TEXT NOT NULL, -- ISO8601
    session_end   TEXT NOT NULL  -- ISO8601
);

-- Fact table (daily aggregates)
CREATE TABLE IF NOT EXISTS fact_player_sessions (
    dt DATE NOT NULL,
    player_id TEXT NOT NULL,
    total_sessions INTEGER NOT NULL,
    total_minutes REAL NOT NULL,
    PRIMARY KEY (dt, player_id)
);
