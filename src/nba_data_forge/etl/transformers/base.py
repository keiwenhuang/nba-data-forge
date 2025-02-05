from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

from nba_data_forge.common.constants.teams import TEAM_MAPPINGS
from nba_data_forge.common.utils.logger import setup_logger
from nba_data_forge.common.utils.paths import paths


class BaseTransformer(ABC):
    """Base class for all transformers"""

    def __init__(self, log_dir: Path | None = None):
        """Initialize base transformer with logging."""
        self.logger = setup_logger(
            self.__class__.__name__, log_dir=log_dir or paths.get_path("logs")
        )
        self.team_mappings = TEAM_MAPPINGS

    def _clean_column(self, df: pd.DataFrame, column: str):
        self.logger.info(f"Cleaning column: {column}")

        try:

            def clean(item):
                if pd.isna(item):
                    return None

                if "." in item:
                    item = str(item).split(".")[1]

                if "_" in item:
                    item = item.replace("_", " ")
                return item

            return df[column].apply(clean)
        except Exception as e:
            self.logger.error(f"Error cleaning column {column}: {str(e)}")
            raise

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform the data"""
        pass
