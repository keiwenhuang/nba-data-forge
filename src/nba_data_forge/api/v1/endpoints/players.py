from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from nba_data_forge.api.dependencies.filters import GameFilters
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


@router.get("/{player_id}/games", response_model=PlayerGameResponse)
async def get_player_games(
    player_id: str,
    filters: GameFilters = Depends(),
    db: Session = Depends(get_session),
) -> PlayerGameResponse:
    """
    Get player's games with optional filters.

    If no season is specified, returns games from current season.
    Use filters to:
    - Get specific season games (season)
    - Get games against specific opponent (opponent)
    - Filter by home/away games (is_home)
    - Filter by wins/losses (is_win)
    - Limit number of returned games (last_n_games)
    """

    service = PlayerStatsService(db)

    # If opponent specified, ignore season filter
    params = {
        "player_id": player_id,
        "is_home": filters.is_home,
        "is_win": filters.is_win,
    }

    if filters.opponent:
        params["opponent_abbrev"] = filters.opponent.upper()
        params["n"] = filters.last_n_games.upper()

    else:
        # Only use season filter if no opponent specified
        params["season"] = filters.season or service.current_season

    averages, games = service.get_player_games(**params)

    if not games:
        detail = f"No games found for player {player_id}"
        if filters.opponent:
            detail += f" vs {filters.opponent}"
        if filters.season:
            detail += f" in season {filters.season}"
        else:
            detail += " in current season"
        if filters.is_home is not None:
            detail += f" {'at home' if filters.is_home else 'away'}"
        if filters.is_win is not None:
            detail += f" ({('wins' if filters.is_win else 'losses')})"
        raise HTTPException(status_code=404, detail=detail)

    return PlayerGameResponse(averages=averages, games=games)
