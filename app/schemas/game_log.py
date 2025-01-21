from datetime import date

from pydantic import BaseModel


class GameLog(BaseModel):
    active: bool
    date: date
    opponent: str
    is_home: bool
    is_win: bool
    minutes_played: float
    made_field_goals: int
    attempted_field_goals: int
    made_three_point_field_goals: int
    attempted_three_point_field_goals: int
    made_free_throws: int
    attempted_free_throws: int
    offensive_rebounds: int
    defensive_rebounds: int
    assists: int
    steals: int
    blocks: int
    turnovers: int
    personal_fouls: int
    points_scored: int
    game_score: float
    plus_minus: int
