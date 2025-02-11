from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from nba_data_forge.api.schemas.boxscore import DailyBoxScores as DailyBoxScoresSchema
from nba_data_forge.api.services.boxscore_service import BoxScoreService
from nba_data_forge.common.db.database import get_session

router = APIRouter()


# TODO: data is not complete
@router.get("/{game_date}", response_model=DailyBoxScoresSchema)
def get_games_by_date(game_date: date, db: Session = Depends(get_session)):
    service = BoxScoreService(db)
    return service.get_daily_boxscores(game_date)
