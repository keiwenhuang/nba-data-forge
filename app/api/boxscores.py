from fastapi import APIRouter
from schemas.boxscore import DailyBoxScores

router = APIRouter(prefix="/api/v1")


@router.get("/boxscores/date/{game_date}", response_model=DailyBoxScores)
def get_games_by_date(game_date):
    pass
