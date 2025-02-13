from sqlalchemy import func, select
from sqlalchemy.orm import Session

from nba_data_forge.api.models.game_log import GameLog


class PlayerStatsService:
    def __init__(self, db: Session):
        self.db = db

    def get_last_n_games(self, player_id: str, n: int = 10):
        # Base query for game logs
        query = self.db.query(GameLog).filter(GameLog.player_id == player_id)

        # Get last N games
        games = query.order_by(GameLog.date.desc()).limit(n).all()

        # Calculate averages
        averages_query = self.db.query(
            func.round(func.avg(GameLog.points_scored), 1).label("avg_points"),
            func.round(func.avg(GameLog.offensive_rebounds), 1).label(
                "avg_offensive_rebounds"
            ),
            func.round(func.avg(GameLog.defensive_rebounds), 1).label(
                "avg_defensive_rebounds"
            ),
            func.round(func.avg(GameLog.assists), 1).label("avg_assists"),
            func.round(func.avg(GameLog.steals), 1).label("avg_steals"),
            func.round(func.avg(GameLog.blocks), 1).label("avg_blocks"),
            func.count().label("games_played"),
        ).filter(GameLog.id.in_([g.id for g in games]))

        averages = averages_query.first()._asdict()

        return averages, [game.to_dict() for game in games]

    def get_games_vs_component(
        self,
        player_id: str,
        opponent_abbrev: str,
        n: int = 5,
        season: int | None = None,
        is_home: bool | None = None,
    ):
        query = self.db.query(GameLog).filter(
            GameLog.player_id == player_id, GameLog.opponent_abbrev == opponent_abbrev
        )

        if season:
            query = query.filter(GameLog.season == season)
        if is_home:
            query = query.filter(GameLog.is_home == is_home)

        query = query.order_by(GameLog.date.desc())
        if n:
            query = query.limit(n)

        games = query.all()

        averages_query = self.db.query(
            func.round(func.avg(GameLog.points_scored), 1).label("avg_points"),
            func.round(func.avg(GameLog.offensive_rebounds), 1).label(
                "avg_offensive_rebounds"
            ),
            func.round(func.avg(GameLog.defensive_rebounds), 1).label(
                "avg_defensive_rebounds"
            ),
            func.round(func.avg(GameLog.assists), 1).label("avg_assists"),
            func.round(func.avg(GameLog.steals), 1).label("avg_steals"),
            func.round(func.avg(GameLog.blocks), 1).label("avg_blocks"),
            func.count().label("games_played"),
        ).filter(GameLog.id.in_([g.id for g in games]))

        averages = averages_query.first()._asdict()

        return averages, [game.to_dict() for game in games]
