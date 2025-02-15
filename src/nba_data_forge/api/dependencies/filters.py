from datetime import date

from fastapi import Query
from pydantic import BaseModel


class GameFilters(BaseModel):
    is_home: bool | None = Query(default=None, description="Filter for home games")
    is_win: bool | None = Query(default=None, description="Filter for wins")


class SeasonFilters(GameFilters):

    season: int | None = Query(
        default=None, description="Season ending year (e.g., 2024 for 2023-24 season)"
    )


class OpponentFilters(GameFilters):

    opponent_abbrev: str | None = Query(
        default=None, description="Opponent team abbreviation (e.g., 'LAL')"
    )
    last_n_games: int | None = Query(default=5, description="Get only the last N games")
