from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from nba_pipeline.api.core.database import get_session
from nba_pipeline.api.dependencies.filters import CommonQueryParams
from nba_pipeline.api.dependencies.query_utils import (
    apply_common_filters,
    check_record_exists,
)
from nba_pipeline.api.models.game_log import GameLog as GameLogModel
from nba_pipeline.api.schemas.game_log import GameLog as GameLogSchema
from nba_pipeline.api.schemas.Player_name_id import PlayerNameID

router = APIRouter()


@router.get("/", response_model=List[PlayerNameID])
async def list_players(db: Session = Depends(get_session)):
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
    # Check if player exists
    if not check_record_exists(db, GameLogModel, player_id=player_id):
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")

    query = db.query(GameLogModel).filter(GameLogModel.player_id == player_id)
    query = apply_common_filters(query, commons)
    return query.all()


@router.get("/{player_id}/vs/{opponent}", response_model=List[GameLogSchema])
async def get_player_vs_opponent_stats(
    player_id: str,
    opponent: str,
    db: Session = Depends(get_session),
    commons: CommonQueryParams = Depends(),
):
    # Check if player exists
    if not check_record_exists(db, GameLogModel, player_id=player_id):
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")

    # Check if opponent exists
    if not check_record_exists(db, GameLogModel, opponent=opponent):
        raise HTTPException(status_code=404, detail=f"Team {opponent} not found")

    query = (
        db.query(GameLogModel)
        .filter(GameLogModel.player_id == player_id)
        .filter(GameLogModel.opponent == opponent)
    )

    query = apply_common_filters(query, commons)
    return query.all()
