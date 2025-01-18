from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.models.game_log import GameLog as GameLogModel
from app.schemas.boxscore import DailyBoxScores as DailyBoxScoresSchema
from app.schemas.boxscore import GameBoxScore as GameBoxScoreSchema
from app.schemas.boxscore import PlayerBoxScore as PlayerBoxScoreSchema
from app.schemas.boxscore import TeamBoxScore as TeamBoxScoreSchema

router = APIRouter()


# TODO: data is not complete
@router.get("/boxscores/date/{game_date}", response_model=DailyBoxScoresSchema)
def get_games_by_date(game_date: date, db: Session = Depends(get_session)):
    """Get box scores for NBA games on a specific date.

    This endpoint returns detailed box score statistics for all NBA games played on the specified date.
    Each game includes both team and individual player statistics.

    Args:
        game_date (date): The date to retrieve box scores for
        db (Session): Database session dependency

    Returns:
        DailyBoxScoresSchema: Object containing list of games with box scores for the specified date
            - date: The requested game date
            - games: List of games played on that date, including:
                - Home and away team details
                - Individual player statistics for both teams

    Raises:
        HTTPException: If no games are found for the specified date
    """
    game_logs = db.query(GameLogModel).filter(GameLogModel.date == game_date).all()
    game_groups = {}
    for log in game_logs:
        teams = sorted([log.team, log.opponent])
        game_key = tuple(teams)
        if game_key not in game_groups:
            game_groups[game_key] = []
        game_groups[game_key].append(log)

    games = []
    for game_logs in game_groups.values():
        home_logs = [log for log in game_logs if log.is_home]
        away_logs = [log for log in game_logs if not log.is_home]

        if not home_logs or not away_logs:
            continue

        home_players = [
            PlayerBoxScoreSchema(
                player_name=log.player_name,
                minutes_played=log.minutes_played,
                made_field_goals=log.made_field_goals,
                attempted_field_goals=log.attempted_field_goals,
                made_three_point_field_goals=log.made_three_point_field_goals,
                attempted_three_point_field_goals=log.attempted_three_point_field_goals,
                made_free_throws=log.made_free_throws,
                attempted_free_throws=log.attempted_free_throws,
                offensive_rebounds=log.offensive_rebounds,
                defensive_rebounds=log.defensive_rebounds,
                assists=log.assists,
                steals=log.steals,
                blocks=log.blocks,
                turnovers=log.turnovers,
                personal_fouls=log.personal_fouls,
                plus_minus=log.plus_minus,
                points_scored=log.points_scored,
            )
            for log in home_logs
        ]

        away_players = [
            PlayerBoxScoreSchema(
                player_name=log.player_name,
                minutes_played=log.minutes_played,
                made_field_goals=log.made_field_goals,
                attempted_field_goals=log.attempted_field_goals,
                made_three_point_field_goals=log.made_three_point_field_goals,
                attempted_three_point_field_goals=log.attempted_three_point_field_goals,
                made_free_throws=log.made_free_throws,
                attempted_free_throws=log.attempted_free_throws,
                offensive_rebounds=log.offensive_rebounds,
                defensive_rebounds=log.defensive_rebounds,
                assists=log.assists,
                steals=log.steals,
                blocks=log.blocks,
                turnovers=log.turnovers,
                personal_fouls=log.personal_fouls,
                plus_minus=log.plus_minus,
                points_scored=log.points_scored,
            )
            for log in away_logs
        ]

        home_team = TeamBoxScoreSchema(
            team=home_logs[0].team,
            is_home=True,
            is_win=home_logs[0].is_win,
            players=home_players,
        )

        away_team = TeamBoxScoreSchema(
            team=away_logs[0].team,
            is_home=False,
            is_win=away_logs[0].is_win,
            players=away_players,
        )

        game = GameBoxScoreSchema(
            game_date=game_date,
            home_team=home_team,
            away_team=away_team,
        )

        games.append(game)

    return DailyBoxScoresSchema(date=game_date, games=games)
