from fastapi import APIRouter

from .endpoints import boxscores, game_logs, players, teams

router = APIRouter(prefix="/v1")

router.include_router(boxscores.router, prefix="/boxscores", tags=["boxscores"])
router.include_router(game_logs.router, prefix="/game_logs", tags=["game_logs"])
router.include_router(players.router, prefix="/players", tags=["players"])
router.include_router(teams.router, prefix="/teams", tags=["teams"])
