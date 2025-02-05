from pathlib import Path

import pandas as pd

from nba_data_forge.common.utils.logger import setup_logger
from nba_data_forge.common.utils.paths import paths


class GameLogTransformer:
    def __init__(self, log_dir: Path | None = None):
        """
        Initialize the transformer with team mappings and logger.

        Args:
            log_dir: Optional directory for logs. Defaults to project_root/logs
        """

        if log_dir is None:
            log_dir = paths.get_path("logs")
        self.logger = setup_logger(__class__.__name__, log_dir=log_dir)
        self.team_mapping = {
            "atlanta hawks": "ATL",
            "boston celtics": "BOS",
            "brooklyn nets": "BKN",
            "charlotte bobcats": "CHA",  # renamed
            "charlotte hornets": "CHA",
            "chicago bulls": "CHI",
            "cleveland cavaliers": "CLE",
            "dallas mavericks": "DAL",
            "denver nuggets": "DEN",
            "detroit pistons": "DET",
            "golden state warriors": "GSW",
            "houston rockets": "HOU",
            "indiana pacers": "IND",
            "los angeles clippers": "LAC",
            "los angeles lakers": "LAL",
            "memphis grizzlies": "MEM",
            "miami heat": "MIA",
            "milwaukee bucks": "MIL",
            "minnesota timberwolves": "MIN",
            "new jersey nets": "BKN",  # relocated
            "new orleans hornets": "NOP",  # renamed
            "new orleans oklahoma city hornets": "NOP",  # temp relocated
            "new orleans pelicans": "NOP",
            "new york knicks": "NYK",
            "oklahoma city thunder": "OKC",
            "orlando magic": "ORL",
            "philadelphia 76ers": "PHI",
            "phoenix suns": "PHX",
            "portland trail blazers": "POR",
            "sacramento kings": "SAC",
            "san antonio spurs": "SAS",
            "seattle supersonics": "OKC",  # relocated
            "toronto raptors": "TOR",
            "utah jazz": "UTA",
            "washington wizards": "WAS",
        }

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

    def transform(self, df: pd.DataFrame):
        """
        Transform game log data with standardized team abbreviations and boolean flags.

        Args:
            df: DataFrame containing game log data

        Returns:
            DataFrame with additional columns:
                - team_abbrev: Standardized team abbreviations
                - opponent_abbrev: Standardized opponent abbreviations
                - is_home: Boolean indicating home games
                - is_win: Boolean indicating wins
        """

        try:
            result = df.copy()

            result["team"] = self._clean_column(result, "team")
            result["opponent"] = self._clean_column(result, "opponent")
            result["location"] = self._clean_column(result, "location")
            result["outcome"] = self._clean_column(result, "outcome")

            result["team_abbrev"] = result["team"].str.lower().map(self.team_mapping)
            result["opponent_abbrev"] = (
                result["opponent"].str.lower().map(self.team_mapping)
            )
            result["is_home"] = result["location"] == "HOME"
            result["is_win"] = result["outcome"] == "WIN"

            result["minutes_played"] = round(df["seconds_played"] / 60, 3)

        except Exception as e:
            self.logger.error(f"Error transforming: {str(e)}")

        return result
