from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict


class PlayerBoxScore(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    player_name: str
    minutes_played: float
    made_field_goals: int
    attempted_field_goals: int
    made_three_point_field_goals: int
    attempted_three_point_field_goals: int
    made_free_throws: int
    attempted_free_throws: int
    offensive_rebounds: int
    defensive_rebounds: int

    @property
    def total_rebounds(self) -> int:
        return self.offensive_rebounds + self.defensive_rebounds

    assists: int
    steals: int
    blocks: int
    turnovers: int
    personal_fouls: int
    plus_minus: int
    points_scored: int


class TeamBoxScore(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    team: str
    is_home: bool
    is_win: bool
    players: List[PlayerBoxScore]

    @property
    def total_minutes(self):
        return sum(player.minutes_played for player in self.players)

    @property
    def total_made_field_goals(self):
        return sum(player.made_field_goals for player in self.players)

    @property
    def total_attempted_field_goals(self):
        return sum(player.attempted_field_goals for player in self.players)

    @property
    def total_made_three_point_field_goals(self):
        return sum(player.made_three_point_field_goals for player in self.players)

    @property
    def total_attempted_three_point_field_goals(self):
        return sum(player.attempted_three_point_field_goals for player in self.players)

    @property
    def total_made_free_throws(self):
        return sum(player.made_free_throws for player in self.players)

    @property
    def total_attempted_free_throws(self):
        return sum(player.attempted_free_throws for player in self.players)

    @property
    def total_offensive_rebounds(self):
        return sum(player.offensive_rebounds for player in self.players)

    @property
    def total_defensive_rebounds(self):
        return sum(player.defensive_rebounds for player in self.players)

    @property
    def total_total_rebounds(self):
        return sum(player.total_rebounds for player in self.players)

    @property
    def total_assists(self):
        return sum(player.assists for player in self.players)

    @property
    def total_steals(self):
        return sum(player.steals for player in self.players)

    @property
    def total_blocks(self):
        return sum(player.blocks for player in self.players)

    @property
    def total_turnovers(self):
        return sum(player.turnovers for player in self.players)

    @property
    def total_personal_fouls(self):
        return sum(player.personal_fouls for player in self.players)

    @property
    def total_score(self) -> int:
        return sum(player.points_scored for player in self.players)


class GameBoxScore(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    game_date: date
    home_team: TeamBoxScore
    away_team: TeamBoxScore


class DailyBoxScores(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    games: List[GameBoxScore]
