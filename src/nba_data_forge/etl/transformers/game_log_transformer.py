import re
from pathlib import Path

import pandas as pd

from nba_data_forge.etl.transformers.base import BaseTransformer


class GameLogTransformer(BaseTransformer):
    def _extract_season(self, filename: str) -> int:
        match = re.search(r"game_logs_(\d{4})\.csv", filename)
        if not match:
            raise ValueError(f"Could not extract season from filename: {filename}")
        return int(match.group(1))

    def transform(self, df: pd.DataFrame, filename: str | None = None):
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

            if filename:
                season = self._extract_season(filename)
                result["season"] = season

            # Clean and standardize team/location/outcome columns
            result["team"] = self._clean_column(result, "team")
            result["opponent"] = self._clean_column(result, "opponent")
            result["location"] = self._clean_column(result, "location")
            result["outcome"] = self._clean_column(result, "outcome")

            # Add team abbreviations
            result["team_abbrev"] = result["team"].str.lower().map(self.team_mappings)
            result["opponent_abbrev"] = (
                result["opponent"].str.lower().map(self.team_mappings)
            )
            # Add boolean flags
            result["is_home"] = result["location"] == "HOME"
            result["is_win"] = result["outcome"] == "WIN"

            result["minutes_played"] = round(df["seconds_played"] / 60, 3)

            self.logger.info(
                f"Transformed {len(result)} game logs with {len(result.columns)} columns"
            )

        except Exception as e:
            self.logger.error(f"Error transforming: {str(e)}")

        return result
