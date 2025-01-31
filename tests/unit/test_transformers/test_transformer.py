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

    def test_win_loss_count(self, transform, sample_data: pd.DataFrame):
        transformed = transform.transform(sample_data)
        original_wins = len(
            sample_data[sample_data["outcome"].isin(["Outcome.WIN", "WIN"])]
        )
        original_loses = len(
            sample_data[sample_data["outcome"].isin(["Outcome.LOSS", "LOSS"])]
        )
        transformed_wins = transformed["is_win"].sum()
        transformed_loses = (~transformed["is_win"]).sum()

        assert original_wins == transformed_wins
        assert original_loses == transformed_loses
        assert len(sample_data) == transformed_wins + transformed_loses

    def test_location_count(self, transform, sample_data: pd.DataFrame):
        transformed = transform.transform(sample_data)
        original_homes = len(
            sample_data[sample_data["location"].isin(["Location.HOME", "HOME"])]
        )
        original_aways = len(
            sample_data[sample_data["location"].isin(["Location.AWAY", "AWAY"])]
        )
        transformed_homes = transformed["is_home"].sum()
        transformed_aways = (~transformed["is_home"]).sum()

        assert original_homes == transformed_homes
        assert original_aways == transformed_aways
        assert len(sample_data) == transformed_homes + transformed_aways
