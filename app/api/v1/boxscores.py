from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.boxscore import DailyBoxScores as DailyBoxScoresSchema
from app.services.boxscore_service import BoxScoreService

router = APIRouter()


# TODO: data is not complete
@router.get("/{game_date}", response_model=DailyBoxScoresSchema)
def get_games_by_date(game_date: date, db: Session = Depends(get_session)):
    service = BoxScoreService(db)
    return service.get_daily_boxscores(game_date)
