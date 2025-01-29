INSERT INTO game_logs (
    date,
    team,
    location,
    opponent,
    outcome,
    active,
    seconds_played,
    made_field_goals,
    attempted_field_goals,
    made_three_point_field_goals,
    attempted_three_point_field_goals,
    made_free_throws,
    attempted_free_throws,
    offensive_rebounds,
    defensive_rebounds,
    assists,
    steals,
    blocks,
    turnovers,
    personal_fouls,
    points_scored,
    game_score,
    plus_minus,
    player_id,
    name,
    team_abbrev,
    opponent_abbrev,
    is_home,
    is_win,
    minutes_played
)
SELECT 
    date,
    team,
    location,
    opponent,
    outcome,
    active,
    seconds_played,
    made_field_goals,
    attempted_field_goals,
    made_three_point_field_goals,
    attempted_three_point_field_goals,
    made_free_throws,
    attempted_free_throws,
    offensive_rebounds,
    defensive_rebounds,
    assists,
    steals,
    blocks,
    turnovers,
    personal_fouls,
    points_scored,
    game_score,
    plus_minus,
    player_id,
    name,
    team_abbrev,
    opponent_abbrev,
    is_home,
    is_win,
    minutes_played
FROM temp_game_logs
ON CONFLICT (date, player_id) 
DO UPDATE SET
    team = EXCLUDED.team,
    location = EXCLUDED.location,
    opponent = EXCLUDED.opponent,
    outcome = EXCLUDED.outcome,
    active = EXCLUDED.active,
    seconds_played = EXCLUDED.seconds_played,
    made_field_goals = EXCLUDED.made_field_goals,
    attempted_field_goals = EXCLUDED.attempted_field_goals,
    made_three_point_field_goals = EXCLUDED.made_three_point_field_goals,
    attempted_three_point_field_goals = EXCLUDED.attempted_three_point_field_goals,
    made_free_throws = EXCLUDED.made_free_throws,
    attempted_free_throws = EXCLUDED.attempted_free_throws,
    offensive_rebounds = EXCLUDED.offensive_rebounds,
    defensive_rebounds = EXCLUDED.defensive_rebounds,
    assists = EXCLUDED.assists,
    steals = EXCLUDED.steals,
    blocks = EXCLUDED.blocks,
    turnovers = EXCLUDED.turnovers,
    personal_fouls = EXCLUDED.personal_fouls,
    points_scored = EXCLUDED.points_scored,
    game_score = EXCLUDED.game_score,
    plus_minus = EXCLUDED.plus_minus,
    name = EXCLUDED.name,
    team_abbrev = EXCLUDED.team_abbrev,
    opponent_abbrev = EXCLUDED.opponent_abbrev,
    is_home = EXCLUDED.is_home,
    is_win = EXCLUDED.is_win,
    minutes_played = EXCLUDED.minutes_played;