from datetime import date, timedelta
from decimal import Decimal

import pytest

from nba_data_forge.api.models.game_log import GameLog
from nba_data_forge.api.services.player_stats_service import PlayerStatsService


class TestPlayerStatsService:
    @pytest.fixture
    def service(self, db_session):
        """Create a PlayerStatsService instance for testing."""

        return PlayerStatsService(db_session)

    @pytest.fixture
    def sample_game_logs(self, db_session):
        """Creates test data set with current and previous season games."""

        base_date = date(2025, 2, 1)
        game_logs = []

        # Create current season games (2024-25)
        for i in range(15):
            game_logs.append(
                GameLog(
                    date=base_date - timedelta(days=i),
                    player_id="test01",
                    name="Test Player",
                    team="Los Angeles Lakers",
                    opponent="Golden State Warriors" if i < 10 else "Dallas Mavericks",
                    team_abbrev="LAL",
                    opponent_abbrev="GSW" if i < 10 else "DAL",
                    is_home=i % 2 == 0,
                    is_win=i % 2 == 0,
                    location="HOME" if i % 2 == 0 else "AWAY",
                    outcome="WIN" if i % 2 == 0 else "LOSS",
                    active=True,
                    seconds_played=30 * 60,
                    minutes_played=30,
                    made_field_goals=8,
                    attempted_field_goals=14,
                    made_three_point_field_goals=2,
                    attempted_three_point_field_goals=5,
                    made_free_throws=4,
                    attempted_free_throws=5,
                    offensive_rebounds=2,
                    defensive_rebounds=5,
                    assists=6,
                    steals=2,
                    blocks=1,
                    turnovers=2,
                    personal_fouls=3,
                    points_scored=22 + i,  # Varying points for average testing
                    game_score=20.5,
                    plus_minus=15.0,
                    season=2025,
                )
            )

        # Add previous season games (2023-24)
        for i in range(3):
            game_logs.append(
                GameLog(
                    date=base_date - timedelta(days=200 + i),
                    player_id="test01",
                    name="Test Player",
                    team="Los Angeles Lakers",
                    opponent="Golden State Warriors",
                    team_abbrev="LAL",
                    opponent_abbrev="GSW",
                    is_home=True,
                    is_win=True,
                    location="HOME",
                    outcome="WIN",
                    active=True,
                    seconds_played=30 * 60,
                    minutes_played=30,
                    made_field_goals=8,
                    attempted_field_goals=14,
                    made_three_point_field_goals=2,
                    attempted_three_point_field_goals=5,
                    made_free_throws=4,
                    attempted_free_throws=5,
                    offensive_rebounds=2,
                    defensive_rebounds=5,
                    assists=6,
                    steals=2,
                    blocks=1,
                    turnovers=2,
                    personal_fouls=3,
                    points_scored=20,
                    game_score=20.5,
                    plus_minus=15.0,
                    season=2024,
                )
            )

        # Add another player for testing get_players_by_season
        game_logs.append(
            GameLog(
                date=base_date,
                player_id="test02",
                name="Another Player",
                team="Boston Celtics",
                opponent="Los Angeles Lakers",
                team_abbrev="BOS",
                opponent_abbrev="LAL",
                is_home=True,
                is_win=True,
                location="HOME",
                outcome="WIN",
                active=True,
                seconds_played=25 * 60,
                minutes_played=25,
                made_field_goals=6,
                attempted_field_goals=12,
                made_three_point_field_goals=2,
                attempted_three_point_field_goals=5,
                made_free_throws=4,
                attempted_free_throws=4,
                offensive_rebounds=1,
                defensive_rebounds=4,
                assists=5,
                steals=2,
                blocks=1,
                turnovers=2,
                personal_fouls=3,
                points_scored=18,
                game_score=15.5,
                plus_minus=10.0,
                season=2025,
            )
        )

        for log in game_logs:
            db_session.add(log)
        db_session.commit()
        return game_logs

    def test_calculate_current_season(self, service):
        """Test current season calculation logic."""

        # During regular season (January)
        service.current_season = 2025
        assert service._calculate_current_season() == 2025

        # During offseason (October)
        test_date = date(2024, 10, 15)
        service.current_season = test_date.year + 1
        assert service._calculate_current_season() == 2025

    def test_get_players_by_season(self, service, sample_game_logs):
        """Test getting all players from a specific season."""

        players = service.get_players_by_season(2025)

        assert len(players) == 2
        assert any(p["player_id"] == "test01" for p in players)
        assert any(p["player_id"] == "test02" for p in players)
        assert all(sorted(p.keys()) == sorted(["player_id", "name"]) for p in players)

    def test_get_player_games_basic(self, service, sample_game_logs):
        """Test getting player games with default parameters."""

        averages, games = service.get_player_games("test01")

        assert len(games) == 10  # Default limit
        assert all(game["player_id"] == "test01" for game in games)
        assert all(game["season"] == 2025 for game in games)
        assert isinstance(averages["avg_points"], Decimal)
        assert isinstance(averages["games_played"], int)
        assert averages["games_played"] == 10

    def test_get_player_games_with_filters(self, service, sample_game_logs):
        """Test getting player games with all filters applied."""

        averages, games = service.get_player_games(
            player_id="test01",
            season=2025,
            opponent_abbrev="GSW",
            is_win=True,
            is_home=True,
            n=5,
        )

        assert len(games) <= 5
        assert all(game["opponent_abbrev"] == "GSW" for game in games)
        assert all(game["is_win"] for game in games)
        assert all(game["is_home"] for game in games)
        assert all(game["season"] == 2025 for game in games)
        assert isinstance(averages["games_played"], int)

    def test_get_player_games_nonexistent_player(self, service, sample_game_logs):
        """Test getting games for nonexistent player."""

        averages, games = service.get_player_games("nonexistent")

        assert len(games) == 0
        assert averages == {"games_played": 0}

    def test_get_player_games_specific_season(self, service, sample_game_logs):
        """Test getting games from a specific season."""

        averages, games = service.get_player_games("test01", season=2024)

        assert len(games) == 3
        assert all(game["season"] == 2024 for game in games)
        assert averages["games_played"] == 3

    def test_get_player_games_averages_calculation(self, service, sample_game_logs):
        """Test that averages calculation includes all expected statistics."""

        averages, _ = service.get_player_games("test01", n=5)

        expected_stats = {
            "avg_points",
            "avg_minutes",
            "avg_made_field_goals",
            "avg_attempted_field_goals",
            "avg_made_threes",
            "avg_attempted_threes",
            "avg_made_free_throws",
            "avg_attempted_free_throws",
            "avg_offensive_rebounds",
            "avg_defensive_rebounds",
            "avg_assists",
            "avg_steals",
            "avg_blocks",
            "avg_turnovers",
            "avg_fouls",
            "avg_game_score",
            "avg_plus_minus",
            "games_played",
        }

        assert set(averages.keys()) == expected_stats
        assert all(isinstance(value, (Decimal, int)) for key, value in averages.items())
        assert isinstance(averages["games_played"], int)

    def test_get_player_games_no_limit(self, service, sample_game_logs):
        """Test getting all player games without limit."""

        averages, games = service.get_player_games("test01", n=None)

        assert len(games) == 15  # All current season games
        assert all(game["season"] == 2025 for game in games)
        assert averages["games_played"] == 15
