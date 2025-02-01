import pandas as pd
import pytest

from nba_data_forge.common.utils.path import get_project_root
from nba_data_forge.etl.transformers.game_log_transformer import GameLogTransformer

ROOT = get_project_root()


class TestDataTransformer:
    @pytest.fixture
    def transform(self):
        """Create a transformer instance for testing"""
        return GameLogTransformer()

    @pytest.fixture
    def sample_data(self):
        df = pd.read_csv(ROOT / "data/raw/game_logs_2004.csv")
        return df.sample(n=30)

    def test_transform_data_integrity(self, transform, sample_data):
        transformed = transform.transform(sample_data)

        # check win/loss counts
        original_wins = len(
            sample_data[sample_data["outcome"].isin(["Outcome.WIN", "WIN"])]
        )
        transformed_wins = transformed["is_win"].sum()
        transformed_losses = (~transformed["is_win"]).sum()

        assert original_wins == transformed_wins
        assert len(sample_data) == transformed_wins + transformed_losses

        # check home/away counts
        original_homes = len(
            sample_data[sample_data["location"].isin(["Location.HOME", "HOME"])]
        )
        transformed_homes = transformed["is_home"].sum()
        transformed_aways = (~transformed["is_home"]).sum()

        assert original_homes == transformed_homes
        assert len(sample_data) == transformed_homes + transformed_aways

    def test_transform_required_columns(self, transform, sample_data):
        """Test presence and types of required columns"""
        transformed = transform.transform(sample_data)

        expected_columns = {
            "team_abbrev": "object",
            "opponent_abbrev": "object",
            "is_home": "bool",
            "is_win": "bool",
            "minutes_played": "float64",
        }

        for col, dtype in expected_columns.items():
            print(col, transformed[col].dtype)
            assert col in transformed.columns
            assert transformed[col].dtype == dtype

    def test_columns_cleaning(self, transform):
        """Test that all relevant columns are properly cleaned"""
        # Create test data with all formats we need to handle
        test_data = pd.DataFrame(
            {
                "team": [
                    "Team.BOSTON_CELTICS",
                    "BOSTON CELTICS",
                    "Team.NEW_YORK_KNICKS",
                ],
                "opponent": [
                    "Team.LOS_ANGELES_LAKERS",
                    "Team.MIAMI_HEAT",
                    "CHICAGO BULLS",
                ],
                "location": ["Location.HOME", "Location.AWAY", "HOME"],
                "outcome": ["Outcome.WIN", "Outcome.LOSS", "WIN"],
            }
        )

        transformed = transform.transform(test_data)

        # Verify team cleaning
        assert transformed["team"].tolist() == [
            "BOSTON CELTICS",
            "BOSTON CELTICS",
            "NEW YORK KNICKS",
        ]

        # Verify opponent cleaning
        assert transformed["opponent"].tolist() == [
            "LOS ANGELES LAKERS",
            "MIAMI HEAT",
            "CHICAGO BULLS",
        ]

        # Verify location cleaning
        assert transformed["location"].tolist() == ["HOME", "AWAY", "HOME"]

        # Verify outcome cleaning
        assert transformed["outcome"].tolist() == ["WIN", "LOSS", "WIN"]
