from typing import List, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from nba_data_forge.api.models.game_log import GameLog
from nba_data_forge.api.schemas.players import PlayerStats


class PlayerService:
    def __init__(self, db: Session):
        self.db = db

    def get_player_list(
        self, skip: int = 0, limit: int = 100
    ) -> Tuple[List[dict], int]:
        """Get list of all players with pagination"""
        # Get total count
        total = self.db.query(func.count(func.distinct(GameLog.player_id))).scalar()

        # Get player list
        query = (
            select(GameLog.player_id, GameLog.name)
            .distinct()
            .order_by(GameLog.name)
            .offset(skip)
            .limit(limit)
        )

        players = self.db.execute(query).all()
        return [{"player_id": p.player_id, "name": p.name} for p in players], total

    def get_player_stats(
        self, player_id: str, season: int | None = None
    ) -> PlayerStats:
        """Get player's statistics, either career or season-specific"""
        query = self.db.query(
            func.count(GameLog.id).label("games_played"),
            func.avg(GameLog.points_scored).label("points_per_game"),
            func.avg(GameLog.offensive_rebounds).label("offensive_rebounds_per_game"),
            func.avg(GameLog.defensive_rebounds).label("defensive_rebounds_per_game"),
            func.avg(GameLog.assists).label("assists_per_game"),
            func.avg(GameLog.steals).label("steals_per_game"),
            func.avg(GameLog.blocks).label("blocks_per_game"),
            func.avg(GameLog.minutes_played).label("minutes_per_game"),
        ).filter(GameLog.player_id == player_id)

        if season is not None:
            query = query.filter(GameLog.season == season)

        stats = query.first()

        if not stats:
            return None

        total_rebound_per_game = (
            stats.offensive_rebounds_per_game + stats.defensive_rebounds_per_game
        )

        return PlayerStats(
            games_played=stats.games_played,
            points_per_game=stats.points_per_game,
            rebounds_per_game=total_rebound_per_game,
            assists_per_game=stats.assists_per_game,
            steals_per_game=stats.steals_per_game,
            blocks_per_game=stats.blocks_per_game,
            minutes_per_game=stats.minutes_per_game,
            season=season,
        )

    def get_player_info(self, player_id: str) -> dict:
        """Get player's basic information"""
        player = self.db.query(GameLog).filter(GameLog.player_id == player_id).first()

        if not player:
            return None

        return {"player_id": player.player_id, "name": player.name}
