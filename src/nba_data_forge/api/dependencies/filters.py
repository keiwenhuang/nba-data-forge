from datetime import date

from fastapi import Query
from pydantic import BaseModel


class CommonQueryParams(BaseModel):
    season: int | None = Query(
        None, description="Season ending year (e.g., 2024 for 2023-24 season)"
    )
    start_date: date | None = Query(
        None, description="Filter games from this date (YYYY-MM-DD)"
    )
    end_date: date | None = Query(
        None, description="Filter games until this date (YYYY-MM-DD)"
    )
    last_n_games: int | None = Query(None, description="Get only the last N games")


class GameFilters(CommonQueryParams):
    """Game filters including opponent and game outcome."""

    opponent: str | None = Query(
        default=None, description="Opponent team abbreviation (e.g., 'LAL')"
    )
    is_home: bool | None = Query(default=None, description="Filter for home games")
    is_win: bool | None = Query(default=None, description="Filter for wins")
