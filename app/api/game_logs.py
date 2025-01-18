from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.models.game_log import GameLog as GameLogModel
from app.schemas.game_log import GameLog as GameLogSchema

router = APIRouter()


@router.get("/game_logs", response_model=List[GameLogSchema])
def get_game_log(db: Session = Depends(get_session)):
    game_logs = db.query(GameLogModel).limit(5).all()
    return game_logs
