from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import distinct
from sqlalchemy.orm import Session

from nba_data_forge.api.dependencies.filters import CommonQueryParams
from nba_data_forge.api.dependencies.query_utils import (
    apply_common_filters,
    check_record_exists,
)
from nba_data_forge.api.models.game_log import GameLog as GameLogModel
from nba_data_forge.api.schemas.game_log import GameLog as GameLogSchema
from nba_data_forge.api.schemas.players import PlayerDetail, PlayerList
from nba_data_forge.api.services.player_service import PlayerService
from nba_data_forge.common.db.database import get_session

router = APIRouter()


@router.get("/", response_model=PlayerList)
async def list_players(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_session),
) -> PlayerList:
    """
    Get list of all players with pagination.
    """
    service = PlayerService(db)
    players, total = service.get_player_list(skip=skip, limit=limit)
    return PlayerList(items=players, total=total)


@router.get("/{player_id}", response_model=PlayerDetail)
async def get_player(
    player_id: str,
    season: int | None = Query(
        default=None, description="Filter stats by season", ge=2003, le=2024
    ),
    db: Session = Depends(get_session),
) -> PlayerDetail:
    """
    Get player's information and statistics.

    Args:
        player_id: Player's unique identifier
        season: Optional season filter (2003-2024)
        db: Database session

    Returns:
        PlayerDetail: Player information with career and optional season statistics
    """
    service = PlayerService(db)

    # Get player info
    player_info = service.get_player_info(player_id)
    if not player_info:
        raise HTTPException(
            status_code=404, detail=f"Player with ID {player_id} not found"
        )

    # Get career stats
    career_stats = service.get_player_stats(player_id)
    if not career_stats:
        raise HTTPException(
            status_code=404, detail=f"Statistics not found for player {player_id}"
        )

    # Get season stats if requested
    season_stats = None
    if season:
        season_stats = service.get_player_stats(player_id, season)
        if not season_stats:
            raise HTTPException(
                status_code=404,
                detail=f"No stats found for player {player_id} in season {season}",
            )

    return PlayerDetail(
        player_id=player_info["player_id"],
        name=player_info["name"],
        career_stats=career_stats,
        season_stats=season_stats,
    )


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
