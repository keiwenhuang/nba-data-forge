from datetime import date

from fastapi import Query
from pydantic import BaseModel


def get_season_date_range(season: int):
    season_start = date(season - 1, 10, 1)
    season_end = date(season, 6, 30)
    return season_start, season_end


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
