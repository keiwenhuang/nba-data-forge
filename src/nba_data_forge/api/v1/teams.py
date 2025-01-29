from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from nba_pipeline.api.core.database import get_session
from nba_pipeline.api.models.game_log import GameLog
from nba_pipeline.api.schemas.team_names import TeamNames

router = APIRouter()


@router.get("/", response_model=List[TeamNames])
async def get_teams(db: Session = Depends(get_session)):
    teams = (
        db.query(GameLog)
        .with_entities(GameLog.team)
        .distinct()
        .order_by(GameLog.team)
        .all()
    )
    return teams
