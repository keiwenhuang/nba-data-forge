from datetime import datetime

import pandas as pd
import pytest

from nba_data_forge.etl.loaders.database import DatabaseLoader


def create_test_data(player_id: str, team: str, date: str, points: int = 20) -> dict:
    """Helper function to create a test record with all required fields"""
    return {
        "player_id": player_id,
        "name": f"Player {player_id}",
        "team": team,
        "location": "HOME",
        "opponent": "CELTICS",
        "outcome": "WIN",
        "seconds_played": 1800,  # 30 minutes
        "made_field_goals": 8,
        "attempted_field_goals": 15,
        "made_three_point_field_goals": 2,
        "attempted_three_point_field_goals": 5,
        "made_free_throws": points
        - (8 - 2) * 2
        - 2 * 3,  # Calculate free throws based on points
        "attempted_free_throws": 4,
        "offensive_rebounds": 1,
        "defensive_rebounds": 5,
        "assists": 4,
        "steals": 2,
        "blocks": 1,
        "turnovers": 2,
        "personal_fouls": 3,
        "plus_minus": 10.0,
        "game_score": 15.5,
        "date": date,
        "team_abbrev": team[:3].upper(),
        "opponent_abbrev": "BOS",
        "is_home": True,
        "is_win": True,
        "minutes_played": 30.0,
        "season": 2024,
        "points_scored": points,
        "active": True,
    }


def test_upsert_functionality():
    """Test the upsert functionality with both new and existing records"""

    # Create test data - first batch
    initial_records = [
        create_test_data("P002", "WARRIORS", "2024-02-01", 30),  # Updated points
        create_test_data("P003", "HEAT", "2024-02-01", 15),  # New record
    ]
    df1 = pd.DataFrame(initial_records)

    # Create test data - second batch (1 new record, 1 update)
    update_records = [
        create_test_data("P002", "WARRIORS", "2024-02-01", 30),  # Updated points
        create_test_data("P004", "HEAT", "2024-02-01", 45),  # New record
    ]
    df2 = pd.DataFrame(update_records)

    # Initialize database loader
    loader = DatabaseLoader(test=True)

    try:
        # First insertion
        print("Inserting initial records...")
        result1 = loader.upsert(
            df=df1, table_name="game_logs", unique_columns=["date", "player_id", "team"]
        )
        print(f"First batch result: {result1} records affected")

        # Second insertion (upsert)
        print("\nUpserting second batch...")
        result2 = loader.upsert(
            df=df2, table_name="game_logs", unique_columns=["date", "player_id", "team"]
        )
        print(f"Second batch result: {result2} records affected")

        # Verify final state
        with loader.engine.connect() as conn:
            result = pd.read_sql(
                "SELECT * FROM game_logs WHERE date = '2024-02-01' ORDER BY player_id",
                conn,
            )
            print("\nFinal state of the table:")
            print(result)

    except Exception as e:
        print(f"Error during test: {str(e)}")
        raise


if __name__ == "__main__":
    test_upsert_functionality()
