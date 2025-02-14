from datetime import date
from typing import Dict, List, Tuple

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from nba_data_forge.api.models.game_log import GameLog


class PlayerStatsService:
    def __init__(self, db: Session):
        self.db = db
        self.current_season = self._calculate_current_season()

    def _calculate_current_season(self) -> int:
        """Calculate current NBA season based on date."""

        today = date.today()
        return today.year + 1 if today.month >= 10 else today.year

    def get_players_by_season(self, season: int) -> List[Dict]:
        """Get all players who played in a specific season with their basic info."""

        query = (
            self.db.query(
                GameLog.player_id,
                GameLog.name,
            )
            .filter(GameLog.season == season)
            .group_by(GameLog.player_id, GameLog.name)
            .order_by(GameLog.name)
        )
        return [row._asdict() for row in query.all()]

    def _calculate_averages(self, game_ids: List[int]) -> Dict:
        """Calculate average statistics for given game IDs."""

        averages_query = self.db.query(
            func.round(func.avg(GameLog.points_scored), 1).label("avg_points"),
            func.round(func.avg(GameLog.minutes_played), 1).label("avg_minutes"),
            func.round(func.avg(GameLog.made_field_goals), 1).label(
                "avg_made_field_goals"
            ),
            func.round(func.avg(GameLog.attempted_field_goals), 1).label(
                "avg_attempted_field_goals"
            ),
            func.round(func.avg(GameLog.made_three_point_field_goals), 1).label(
                "avg_made_threes"
            ),
            func.round(func.avg(GameLog.attempted_three_point_field_goals), 1).label(
                "avg_attempted_threes"
            ),
            func.round(func.avg(GameLog.made_free_throws), 1).label(
                "avg_made_free_throws"
            ),
            func.round(func.avg(GameLog.attempted_free_throws), 1).label(
                "avg_attempted_free_throws"
            ),
            func.round(func.avg(GameLog.offensive_rebounds), 1).label(
                "avg_offensive_rebounds"
            ),
            func.round(func.avg(GameLog.defensive_rebounds), 1).label(
                "avg_defensive_rebounds"
            ),
            func.round(func.avg(GameLog.assists), 1).label("avg_assists"),
            func.round(func.avg(GameLog.steals), 1).label("avg_steals"),
            func.round(func.avg(GameLog.blocks), 1).label("avg_blocks"),
            func.round(func.avg(GameLog.turnovers), 1).label("avg_turnovers"),
            func.round(func.avg(GameLog.personal_fouls), 1).label("avg_fouls"),
            func.round(func.avg(GameLog.game_score), 1).label("avg_game_score"),
            func.round(func.avg(GameLog.plus_minus), 1).label("avg_plus_minus"),
        ).filter(GameLog.id.in_(game_ids))

        return averages_query.first()._asdict()

    def get_player_games(
        self,
        player_id: str,
        season: int | None = None,
        opponent_abbrev: str | None = None,
        is_win: bool | None = None,
        is_home: bool | None = None,
        n: int | None = None,
    ) -> Tuple[Dict, List[Dict]]:
        """Get player's games with optional filters."""

        conditions = [GameLog.player_id == player_id]

        if season is None:
            conditions.append(GameLog.season == self.current_season)
        else:
            conditions.append(GameLog.season == season)

        if opponent_abbrev:
            conditions.append(GameLog.opponent_abbrev == opponent_abbrev)
        if is_win is not None:
            conditions.append(GameLog.is_win == is_win)
        if is_home is not None:
            conditions.append(GameLog.is_home == is_home)

        query = (
            self.db.query(GameLog)
            .filter(and_(*conditions))
            .order_by(GameLog.date.desc())
        )

        if n:
            query = query.limit(n)

        games = query.all()

        if not games:
            return {"games_played": 0}, []

        averages = self._calculate_averages([g.id for g in games])
        averages["games_played"] = len(games)  # Add games_played count
        return averages, [game.to_dict() for game in games]
