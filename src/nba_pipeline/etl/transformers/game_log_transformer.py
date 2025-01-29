from pathlib import Path

import pandas as pd
from etl.utils.logger import setup_logger
from etl.utils.path import get_project_root


class GameLogTransformer:
    def __init__(self, log_dir: Path | None = None):
        """
        Initialize the transformer with team mappings and logger.

        Args:
            log_dir: Optional directory for logs. Defaults to project_root/logs
        """

        if log_dir is None:
            log_dir = get_project_root() / "logs"
        self.logger = setup_logger(__class__.__name__, log_dir=log_dir)
        self.team_mapping = {
            "atlanta hawks": "ATL",
            "boston celtics": "BOS",
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
            "new york knicks": "NYK",
            "orlando magic": "ORL",
            "philadelphia 76ers": "PHI",
            "phoenix suns": "PHX",
            "portland trail blazers": "POR",
            "sacramento kings": "SAC",
            "san antonio spurs": "SAS",
            "seattle supersonics": "OKC",  # relocated
            "toronto raptors": "TOR",
            "team.atlanta_hawks": "ATL",
            "team.boston_celtics": "BOS",
            "team.brooklyn_nets": "BKN",  # relocated
            "team.charlotte_bobcats": "CHA",  # renamed
            "team.charlotte_hornets": "CHA",
            "team.chicago_bulls": "CHI",
            "team.cleveland_cavaliers": "CLE",
            "team.dallas_mavericks": "DAL",
            "team.denver_nuggets": "DEN",
            "team.detroit_pistons": "DET",
            "team.golden_state_warriors": "GSW",
            "team.houston_rockets": "HOU",
            "team.indiana_pacers": "IND",
            "team.los_angeles_clippers": "LAC",
            "team.los_angeles_lakers": "LAL",
            "team.memphis_grizzlies": "MEM",
            "team.miami_heat": "MIA",
            "team.milwaukee_bucks": "MIL",
            "team.minnesota_timberwolves": "MIN",
            "team.new_jersey_nets": "BKN",  # relocated
            "team.new_orleans_hornets": "NOP",  # renamed
            "team.new_orleans_oklahoma_city_hornets": "NOP",  # temp relocated
            "team.new_orleans_pelicans": "NOP",
            "team.new_york_knicks": "NYK",
            "team.oklahoma_city_thunder": "OKC",
            "team.orlando_magic": "ORL",
            "team.philadelphia_76ers": "PHI",
            "team.phoenix_suns": "PHX",
            "team.portland_trail_blazers": "POR",
            "team.sacramento_kings": "SAC",
            "team.san_antonio_spurs": "SAS",
            "team.seattle_supersonics": "OKC",  # relocated
            "team.toronto_raptors": "TOR",
            "team.utah_jazz": "UTA",
            "team.washington_wizards": "WAS",
            "utah jazz": "UTA",
            "washington wizards": "WAS",
        }

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
            result["team_abbrev"] = result["team"].str.lower().map(self.team_mapping)
            result["opponent_abbrev"] = (
                result["opponent"].str.lower().map(self.team_mapping)
            )
            result["is_home"] = result["location"].isin(["Location.HOME", "HOME"])
            result["is_win"] = result["outcome"].isin(["Outcome.WIN", "WIN"])
            result["minutes_played"] = round(df["seconds_played"] / 60, 3)

        except Exception as e:
            self.logger.error(f"Error transforming: {str(e)}")

        return result
