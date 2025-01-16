from datetime import date

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")


@router.get("/player/{player_id}")
async def get_player_stats(
    player_id: str, start_date: date | None = None, end_date: date | None = None
):
    pass


@router.get("/players/{player_id}/averages")
async def get_player_averages(player_id: str, last_n_games: int | None = None):
    pass
