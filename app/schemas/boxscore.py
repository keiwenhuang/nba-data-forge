from datetime import date
from typing import List

from pydantic import BaseModel


class PlayerBoxScore(BaseModel):
    player_name: str
    minutes_played: float
    points_scored: int
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
    plus_minus: int

    @property
    def field_goal_percentage(self):
        return (
            (self.made_field_goals / self.attempted_field_goals * 100)
            if self.attempted_field_goals > 0
            else 0.0
        )

    @property
    def three_point_field_goals_percentage(self):
        return (
            (
                self.made_three_point_field_goals
                / self.attempted_three_point_field_goals
                * 100
            )
            if self.attempted_field_goals > 0
            else 0.0
        )

    @property
    def free_throw_goals_percentage(self):
        return (
            (self.made_free_throws / self.attempted_free_throws * 100)
            if self.attempted_field_goals > 0
            else 0.0
        )

    @property
    def total_rebounds(self):
        return self.offensive_rebounds + self.defensive_rebounds


class TeamBoxScore(BaseModel):
    team_name: str
    is_home: bool
    is_win: bool
    final_score: int
    players: List[PlayerBoxScore]


class GameBoxScore(BaseModel):
    game_date: date
    home_team: TeamBoxScore
    away_team: TeamBoxScore


class DailyBoxScores(BaseModel):
    date: date
    games: List[GameBoxScore]
