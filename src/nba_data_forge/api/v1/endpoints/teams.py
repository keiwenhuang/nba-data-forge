from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from nba_data_forge.api.models.game_log import GameLog
from nba_data_forge.api.schemas.team_names import TeamNames
from nba_data_forge.api.services.team_service import TeamService
from nba_data_forge.common.db.database import get_session

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


@router.get("/abbreviations", response_model=List[str])
async def get_team_abbreviations(db: Session = Depends(get_session)) -> List[str]:
    """Get list of all team abbreviations."""

    service = TeamService(db)
    return service.get_team_abbreviations()
