from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies.filters import CommonQueryParams, get_season_date_range
from app.core.database import get_session
from app.models.game_log import GameLog as GameLogModel
from app.schemas.game_log import GameLog as GameLogSchema
from app.schemas.Player_name_id import PlayerNameID

router = APIRouter()


@router.get("/", response_model=List[PlayerNameID])
async def get_player_names_ids(db: Session = Depends(get_session)):
    players = (
        db.query(GameLogModel)
        .with_entities(GameLogModel.player_id, GameLogModel.player_name)
        .distinct()
        .order_by(GameLogModel.player_name)  # Sort alphabetically
        .all()
    )

    return players


@router.get("/{player_id}/stats", response_model=List[GameLogSchema])
async def get_player_stats(
    player_id: str,
    db: Session = Depends(get_session),
    commons: CommonQueryParams = Depends(),
):
    # base query
    query = db.query(GameLogModel).filter(GameLogModel.player_id == player_id)

    if commons.season:
        season_start, season_end = get_season_date_range(commons.season)
        query = query.filter(
            GameLogModel.date >= season_start, GameLogModel.date <= season_end
        )
    else:
        # If no season specified, use explicit date filters if provided
        if commons.start_date:
            query = query.filter(GameLogModel.date >= commons.start_date)
        if commons.end_date:
            query = query.filter(GameLogModel.date <= commons.end_date)

    query = query.order_by(GameLogModel.date.desc())

    if commons.last_n_games:
        query = query.limit(commons.last_n_games)

    return query.all()
