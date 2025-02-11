from typing import List

from pydantic import BaseModel, Field


class PlayerStats(BaseModel):
    points_per_game: float = Field(..., round=1)
    rebounds_per_game: float = Field(..., round=1)
    assists_per_game: float = Field(..., round=1)
    steals_per_game: float = Field(..., round=1)
    blocks_per_game: float = Field(..., round=1)
    minutes_per_game: float = Field(..., round=1)
    games_played: int
    season: int | None = None

    class Config:
        from_attributes = True


class PlayerBase(BaseModel):
    player_id: str = Field(..., description="Player's unique identifier")
    name: str = Field(..., description="Player's full name")

    class Config:
        from_attributes = True


class PlayerDetail(PlayerBase):
    career_stats: PlayerStats
    season_stats: PlayerStats | None = None

    class Config:
        from_attributes = True


class PlayerList(BaseModel):
    items: List[PlayerBase]
    total: int
