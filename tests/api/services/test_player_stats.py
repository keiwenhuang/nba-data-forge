from datetime import date, timedelta
from decimal import Decimal

import pytest

from nba_data_forge.api.models.game_log import GameLog
from nba_data_forge.api.services.player_stats_service import PlayerStatsService


class TestPlayerStatsService:

    @pytest.fixture
    def service(self, db_session):
        return PlayerStatsService(db_session)

    @pytest.fixture
    def sample_game_logs(self, db_session):
        """Creates test data set with current and previous season games."""

        base_date = date(2025, 2, 1)
        game_logs = []

        # Create 15 current season games
        for i in range(15):
            game_logs.append(
                GameLog(
                    date=base_date - timedelta(days=i),
                    player_id="test01",
                    name="Test Tester",
                    team="Los Angeles Lakers",
                    opponent="Golden States Warriors" if i < 10 else "Dallas Mavs",
                    team_abbrev="LAL",
                    opponent_abbrev="GSW" if i < 10 else "DAL",
                    is_home=i % 2 == 0,
                    is_win=i % 2 == 0,
                    location="HOME" if i % 2 == 0 else "AWAY",
                    outcome="WIN" if i % 2 == 0 else "LOSE",
                    active=True,
                    seconds_played=30 * 60,
                    minutes_played=30,
                    made_field_goals=8,
                    attempted_field_goals=14,
                    made_three_point_field_goals=4,
                    attempted_three_point_field_goals=7,
                    made_free_throws=6,
                    attempted_free_throws=7,
                    offensive_rebounds=2,
                    defensive_rebounds=5,
                    assists=6,
                    steals=3,
                    blocks=2,
                    turnovers=3,
                    personal_fouls=2,
                    points_scored=30 + i,
                    game_score=10.0,
                    plus_minus=10.0,
                    season=2025,
                )
            )

        # Add 3 games from previous season
        for i in range(3):
            game_logs.append(
                GameLog(
                    date=base_date - timedelta(days=200 + i),
                    player_id="test01",
                    name="Test Tester",
                    team="Los Angeles Lakers",
                    opponent="Golden States Warriors" if i % 2 == 0 else "Dallas Mavs",
                    team_abbrev="LAL",
                    opponent_abbrev="GSW" if i % 2 == 0 else "DAL",
                    is_home=i % 2 == 0,
                    is_win=i % 2 == 0,
                    location="HOME" if i % 2 == 0 else "AWAY",
                    outcome="WIN" if i % 2 == 0 else "LOSE",
                    active=True,
                    seconds_played=30 * 60,
                    minutes_played=30,
                    made_field_goals=8,
                    attempted_field_goals=14,
                    made_three_point_field_goals=4,
                    attempted_three_point_field_goals=7,
                    made_free_throws=6,
                    attempted_free_throws=7,
                    offensive_rebounds=2,
                    defensive_rebounds=5,
                    assists=6,
                    steals=3,
                    blocks=2,
                    turnovers=3,
                    personal_fouls=2,
                    points_scored=30 + i,
                    game_score=10.0,
                    plus_minus=10.0,
                    season=2024,
                )
            )

        for log in game_logs:
            db_session.add(log)
        db_session.commit()
        return game_logs

    # test default behavior, n = 10
    def test_get_last_n_games_default(self, service, sample_game_logs):
        averages, games = service.get_last_n_games("test01")

        assert len(games) == 10
        assert games[0]["date"] == date(2025, 2, 1)
        assert averages["games_played"] == 10
        assert isinstance(averages["avg_points"], Decimal)
        assert isinstance(averages["avg_assists"], Decimal)

    # test custom limit, n = 5
    def test_get_last_n_games_custom_limit(self, service, sample_game_logs):
        averages, games = service.get_last_n_games("test01", n=5)
        assert len(games) == 5
        assert all(game["player_id"] == "test01" for game in games)

    # test default behavior with opponent
    def test_get_games_vs_opponent(self, service, sample_game_logs):
        averages, games = service.get_games_vs_component(
            player_id="test01", opponent_abbrev="GSW"
        )
        assert all(game["opponent_abbrev"] == "GSW" for game in games)
        assert averages["games_played"] == len(games)

    # test season filter
    def test_get_games_vs_opponent_with_season(self, service, sample_game_logs):
        averages, games = service.get_games_vs_component(
            player_id="test01", opponent_abbrev="GSW", season=2024
        )
        assert all(game["season"] == 2024 for game in games)
        assert all(game["opponent_abbrev"] == "GSW" for game in games)

    # test home games filter
    def test_get_games_vs_opponent_home_only(self, service, sample_game_logs):
        averages, games = service.get_games_vs_component(
            player_id="test01", opponent_abbrev="GSW", is_home=True
        )
        assert all(game["is_home"] for game in games)
        assert all(game["opponent_abbrev"] == "GSW" for game in games)

    # test limit with opponent
    def test_get_games_vs_opponent_with_limit(self, service, sample_game_logs):
        averages, games = service.get_games_vs_component(
            player_id="test01", opponent_abbrev="GSW", n=2
        )
        assert len(games) == 2
        assert all(game["opponent_abbrev"] == "GSW" for game in games)

    # test edge case
    def test_get_games_nonexistent_player(self, service, sample_game_logs):
        averages, games = service.get_last_n_games("nonexistent-player")
        assert len(games) == 0
        assert averages["games_played"] == 0

    # test edge case
    def test_get_games_vs_nonexistent_opponent(self, service, sample_game_logs):
        averages, games = service.get_games_vs_component(
            player_id="test01", opponent_abbrev="XXX"
        )
        assert len(games) == 0
        assert averages["games_played"] == 0
