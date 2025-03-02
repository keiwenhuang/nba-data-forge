ALTER TABLE IF EXISTS game_logs 
    DROP CONSTRAINT IF EXISTS unique_game_player;


ALTER TABLE game_logs 
    ADD CONSTRAINT unique_game_player 
    UNIQUE (date, player_id, team, game_score);


ALTER TABLE game_logs 
    ADD COLUMN team_abbrev CHAR(3),
    ADD COLUMN opponent_abbrev CHAR(3);


CREATE TABLE game_logs_backup AS SELECT * FROM game_logs;


ALTER TABLE game_logs 
ADD CONSTRAINT game_logs_unique_game 
UNIQUE (date, player_id, team);


ALTER TABLE game_logs 
ALTER COLUMN plus_minus TYPE NUMERIC(5,1);