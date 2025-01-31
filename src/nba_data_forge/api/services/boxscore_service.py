from datetime import date
from typing import List

from sqlalchemy.orm import Session

from nba_data_forge.api.models.game_log import GameLog as GameLogModel
from nba_data_forge.api.schemas.boxscore import (
    DailyBoxScores,
    GameBoxScore,
    PlayerBoxScore,
    TeamBoxScore,
)


class BoxScoreService:
    def __init__(self, db: Session):
        self.db = db

    def _create_player_boxscore(self, log: GameLogModel):
        return PlayerBoxScore.model_validate(log)

    def _create_team_box_score(self, logs: GameLogModel, is_home: bool):
        return TeamBoxScore(
            team=logs[0].team,
            is_home=is_home,
            is_win=logs[0].is_win,
            players=[self._create_player_boxscore(log) for log in logs],
        )

    def _group_game_logs(self, logs: List[GameLogModel]):
        game_groups = {}
        for log in logs:
            teams = tuple(sorted([log.team, log.opponent]))
            if teams not in game_groups:
                game_groups[teams] = []
            game_groups[teams].append(log)
        return game_groups

    def get_daily_boxscores(self, game_date: date) -> DailyBoxScores:
        game_logs = (
            self.db.query(GameLogModel).filter(GameLogModel.date == game_date).all()
        )
        game_groups = self._group_game_logs(game_logs)

        games = []
        for game_logs in game_groups.values():
            home_logs = [log for log in game_logs if log.is_home]
            away_logs = [log for log in game_logs if not log.is_home]

            if not home_logs or not away_logs:
                continue

            game = GameBoxScore(
                game_date=game_date,
                home_team=self._create_team_box_score(home_logs, is_home=True),
                away_team=self._create_team_box_score(away_logs, is_home=False),
            )
            games.append(game)

        return DailyBoxScores(date=game_date, games=games)
