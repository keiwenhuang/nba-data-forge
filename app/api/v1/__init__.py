from fastapi import APIRouter

from .boxscores import router as boxscores_router
from .game_logs import router as game_logs_router
from .players import router as players_router
from .teams import router as teams_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(boxscores_router, prefix="/boxscores")
v1_router.include_router(game_logs_router, prefix="/game_logs")
v1_router.include_router(players_router, prefix="/players")
v1_router.include_router(teams_router, prefix="/teams")
