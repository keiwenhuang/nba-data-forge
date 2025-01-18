from .boxscores import router as boxscores_router
from .game_logs import router as game_logs_router

# Export the routers with their designated names
__all__ = ["game_logs_router", "boxscores_router"]
