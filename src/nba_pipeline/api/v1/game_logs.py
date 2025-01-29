from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from nba_pipeline.api.core.database import get_session
from nba_pipeline.api.models.game_log import GameLog as GameLogModel
from nba_pipeline.api.schemas.game_log import GameLog as GameLogSchema

router = APIRouter()


@router.get("/", response_model=List[GameLogSchema])
def get_game_log(db: Session = Depends(get_session)):
    game_logs = db.query(GameLogModel).limit(5).all()
    return game_logs
