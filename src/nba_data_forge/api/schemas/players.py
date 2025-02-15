from datetime import date
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    """Base schema with common configurations."""

    model_config = ConfigDict(
        from_attributes=True,
        strict=True,
        validate_assignment=True,
        str_strip_whitespace=True,
    )


class PlayerBase(BaseSchema):
    """Base player schema with core player information."""

    player_id: str = Field(description="Player's unique identifier")
    name: str = Field(description="Player's full name")


class PlayerAverageStats(BaseSchema):
    """Schema for player's average statistics."""

    avg_points: Decimal | None = Field(
        default=None, description="Average points per game"
    )
    avg_minutes: Decimal | None = Field(
        default=None, description="Average minutes played"
    )
    avg_made_field_goals: Decimal | None = Field(
        default=None, description="Average field goals made"
    )
    avg_attempted_field_goals: Decimal | None = Field(
        default=None, description="Average field goals attempted"
    )
    avg_made_threes: Decimal | None = Field(
        default=None, description="Average three pointers made"
    )
    avg_attempted_threes: Decimal | None = Field(
        default=None, description="Average three pointers attempted"
    )
    avg_made_free_throws: Decimal | None = Field(
        default=None, description="Average free throws made"
    )
    avg_attempted_free_throws: Decimal | None = Field(
        default=None, description="Average free throws attempted"
    )
    avg_offensive_rebounds: Decimal | None = Field(
        default=None, description="Average offensive rebounds"
    )
    avg_defensive_rebounds: Decimal | None = Field(
        default=None, description="Average defensive rebounds"
    )
    avg_assists: Decimal | None = Field(default=None, description="Average assists")
    avg_steals: Decimal | None = Field(default=None, description="Average steals")
    avg_blocks: Decimal | None = Field(default=None, description="Average blocks")
    avg_turnovers: Decimal | None = Field(default=None, description="Average turnovers")
    avg_fouls: Decimal | None = Field(
        default=None, description="Average personal fouls"
    )
    avg_game_score: Decimal | None = Field(
        default=None, description="Average game score"
    )
    avg_plus_minus: Decimal | None = Field(
        default=None, description="Average plus/minus"
    )


class PlayerGameStats(BaseSchema):
    """Schema for single game statistics."""

    # Game Information
    date: date
    season: int

    # Player Information
    player_id: str
    name: str

    # Team Information
    team: str
    team_abbrev: str
    opponent: str
    opponent_abbrev: str

    # Game Context
    is_home: bool
    is_win: bool
    location: str
    outcome: str
    active: bool

    # Playing Time
    seconds_played: int
    minutes_played: Decimal

    # Shooting Stats
    made_field_goals: int
    attempted_field_goals: int
    made_three_point_field_goals: int
    attempted_three_point_field_goals: int
    made_free_throws: int
    attempted_free_throws: int

    # Box Score Stats
    points_scored: int
    offensive_rebounds: int
    defensive_rebounds: int
    assists: int
    steals: int
    blocks: int
    turnovers: int
    personal_fouls: int

    # Advanced Stats
    game_score: Decimal
    plus_minus: Decimal


# class PlayerStats(BaseSchema):
#     """Schema for player statistics response."""

#     player: PlayerBase
#     averages: PlayerAverageStats
#     games: List[PlayerGameStats]


class PlayerSeasonStats(BaseSchema):
    """Schema for player season statistics."""

    player: PlayerBase
    season: int
    averages: PlayerAverageStats
    games: List[PlayerGameStats]


class PlayerGameResponse(BaseSchema):
    """Schema for game response including averages and game details."""

    averages: PlayerAverageStats
    games: List[PlayerGameStats]
