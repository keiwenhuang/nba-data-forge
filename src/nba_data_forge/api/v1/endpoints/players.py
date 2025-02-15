from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from nba_data_forge.api.dependencies.filters import OpponentFilters, SeasonFilters
from nba_data_forge.api.schemas.players import PlayerBase, PlayerGameResponse
from nba_data_forge.api.services.player_stats_service import PlayerStatsService
from nba_data_forge.common.db.database import get_session

router = APIRouter()


@router.get("/", response_model=List[PlayerBase])
async def list_players(
    season: int = Query(..., ge=2004, le=2025, description="NBA season year"),
    db: Session = Depends(get_session),
) -> List[PlayerBase]:
    """Get list of all players for a specific season."""

    service = PlayerStatsService(db)
    return service.get_players_by_season(season)


@router.get("/{player_id}/season/{season}", response_model=PlayerGameResponse)
async def get_player_games(
    player_id: str,
    season: int,
    filters: SeasonFilters = Depends(),
    db: Session = Depends(get_session),
) -> PlayerGameResponse:
    """Get player's games with optional filters."""

    service = PlayerStatsService(db)

    # If opponent specified, ignore season filter
    params = {"player_id": player_id, "season": season}

    if filters.is_win:
        params["is_win"] = filters.is_win
    if filters.is_home:
        params["is_home"] = filters.is_home

    averages, games = service.get_season_games(**params)

    if not games:
        detail = f"No games found for player {player_id}"
        if season:
            detail += f" in season {season}"
        if filters.is_home is not None:
            detail += f" {'at home' if filters.is_home else 'away'}"
        if filters.is_win is not None:
            detail += f" ({('wins' if filters.is_win else 'losses')})"
        raise HTTPException(status_code=404, detail=detail)

    return PlayerGameResponse(averages=averages, games=games)


@router.get("/{player_id}/vs-opponent-stats", response_model=PlayerGameResponse)
async def get_player_games(
    player_id: str,
    filters: OpponentFilters = Depends(),
    db: Session = Depends(get_session),
) -> PlayerGameResponse:
    """Get player's games with optional filters."""

    service = PlayerStatsService(db)

    # If opponent specified, ignore season filter
    params = {"player_id": player_id}

    if filters.opponent_abbrev:
        params["opponent_abbrev"] = filters.opponent_abbrev
    if filters.is_win:
        params["is_win"] = filters.is_win
    if filters.is_home:
        params["is_home"] = filters.is_home
    if filters.last_n_games:
        params["last_n_games"] = filters.last_n_games

    averages, games = service.get_opponent_stats(**params)

    if not games:
        detail = f"No games found for player {player_id}"
        if filters.opponent_abbrev:
            detail += f" vs {filters.opponent_abbrev}"
        if filters.is_win is not None:
            detail += f" ({('wins' if filters.is_win else 'losses')})"
        if filters.is_home is not None:
            detail += f" {'at home' if filters.is_home else 'away'}"
        raise HTTPException(status_code=404, detail=detail)

    return PlayerGameResponse(averages=averages, games=games)
