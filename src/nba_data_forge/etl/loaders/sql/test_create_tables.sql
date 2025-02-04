CREATE TABLE IF NOT EXISTS test_game_logs (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    team VARCHAR NOT NULL,
    location VARCHAR NOT NULL,
    opponent VARCHAR NOT NULL,
    outcome VARCHAR NOT NULL,
    active BOOLEAN NOT NULL,
    seconds_played INTEGER NOT NULL,
    made_field_goals INTEGER NOT NULL,
    attempted_field_goals INTEGER NOT NULL,
    made_three_point_field_goals INTEGER NOT NULL,
    attempted_three_point_field_goals INTEGER NOT NULL,
    made_free_throws INTEGER NOT NULL,
    attempted_free_throws INTEGER NOT NULL,
    offensive_rebounds INTEGER NOT NULL,
    defensive_rebounds INTEGER NOT NULL,
    assists INTEGER NOT NULL,
    steals INTEGER NOT NULL,
    blocks INTEGER NOT NULL,
    turnovers INTEGER NOT NULL,
    personal_fouls INTEGER NOT NULL,
    points_scored INTEGER NOT NULL,
    game_score DECIMAL(10,1) NOT NULL,
    plus_minus INTEGER NOT NULL,
    player_id VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    team_abbrev CHAR(3) NOT NULL,
    opponent_abbrev CHAR(3) NOT NULL,
    is_home BOOLEAN NOT NULL,
    is_win BOOLEAN NOT NULL,
    minutes_played DECIMAL(10,3) NOT NULL,
    CONSTRAINT unique_player UNIQUE (date, player_id, team, game_score)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_game_logs_player_id ON game_logs(player_id);
CREATE INDEX IF NOT EXISTS idx_game_logs_date ON game_logs(date);
CREATE INDEX IF NOT EXISTS idx_game_logs_player_date ON game_logs(player_id, date);