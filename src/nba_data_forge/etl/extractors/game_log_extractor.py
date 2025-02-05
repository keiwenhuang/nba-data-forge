from datetime import date, timedelta
from pathlib import Path

import pandas as pd
from basketball_reference_web_scraper import client

from nba_data_forge.common.utils.checkpoint import CheckpointManager
from nba_data_forge.etl.extractors.base import BaseExtractor

DEFAULT_TO_SEASON = 2024


class GameLogExtractor(BaseExtractor):
    def __init__(self, max_retries: int = 3, checkpoint_dir=None):
        super().__init__()
        self.max_retries = max_retries
        self.checkpoint_dir = checkpoint_dir
        self.checkpoint_manager = CheckpointManager()

    def _get_game_logs(self, player_id: str, season: int):
        for attempt in range(self.max_retries):
            try:
                self._api_delay()
                return client.regular_season_player_box_scores(
                    player_identifier=player_id, season_end_year=season
                )
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                self.logger.warning(
                    f"Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}. Retrying..."
                )
                self._api_delay((5, 15))

    def _get_game_logs_by_date(self, date: date):
        for attempt in range(self.max_retries):
            try:
                self._api_delay()
                return client.player_box_scores(
                    day=date.day, month=date.month, year=date.year
                )
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                self.logger.warning(
                    f"Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}. Retrying..."
                )
                self._api_delay((5, 15))

    def extract_date_range(self, start_date: date, end_date: date):
        self.logger.info(f"Extracting game logs from {start_date} to {end_date}")
        all_games = []

        current_date = start_date

        while current_date <= end_date:
            try:
                self.logger.info(f"Processing date: {current_date}")
                daily_games = self._get_game_logs_by_date(current_date)

                if daily_games:
                    for game in daily_games:
                        game["date"] = current_date
                    all_games.extend(daily_games)

                self.logger.info(f"Found {len(all_games)} games on {current_date}")

            except Exception as e:
                self.logger.error(
                    f"Error extracting game logs for date {current_date}: {str(e)}"
                )

            current_date += timedelta(days=1)

        if not all_games:
            self.logger.warning("No games found in date range")
            return pd.DataFrame()

        df = pd.DataFrame(all_games)
        self.validate(df)
        self.logger.info(
            f"Extraction complete for date range. Total records: {len(df)}"
        )
        return df

    def extract(self, players_df: pd.DataFrame, season: int) -> pd.DataFrame:
        self.logger.info(f"Processing {season-1}-{season}")
        checkpoint = self.checkpoint_manager.load_latest_checkpoint(season=season)
        season_data = checkpoint["data"] if checkpoint else []
        last_idx = checkpoint["idx"] if checkpoint else 0
        eligible_players = players_df[
            (players_df["year_min"] <= season) & (players_df["year_max"] >= season)
        ]
        self.logger.info(
            f"[Season {season-1}-{season}] Found {len(eligible_players)} eligible players"
        )

        for idx, (_, player) in enumerate(
            eligible_players.iloc[last_idx:].iterrows(), last_idx + 1
        ):
            try:
                self.logger.info(
                    f"[Player {idx}/{len(eligible_players)}] Processing {player['name']} "
                    f"({player['player_id']}) | Season {season-1}-{season}"
                )

                season_game_logs = self._get_game_logs(player["player_id"], season)
                for game_log in season_game_logs:
                    game_log["player_id"] = player["player_id"]
                    game_log["name"] = player["name"]

                season_data.extend(season_game_logs)
                self.checkpoint_manager.save_checkpoint(
                    season, idx, season_data, self.logger
                )

                self.logger.info(
                    f"[Player {idx}/{len(eligible_players)}] Success: {player['name']} | "
                    f"Games extracted: {len(season_game_logs)} | Season {season-1}-{season}"
                )
            except Exception as e:
                error_msg = (
                    f"[Player {idx}/{len(eligible_players)}] Failed: {player['name']} "
                    f"({player['player_id']}) | Season {season-1}-{season} | Error: {str(e)}"
                )
                self.logger.error(error_msg)

        df = pd.json_normalize(season_data)
        self.validate(df)
        self.logger.info(
            f"Extraction complete | Total records: {len(df)} | "
            f"Seasons: {season-1}-{season} | Players: {len(eligible_players)}"
        )
        return df

    def validate(self, df):
        if df.empty:
            raise ValueError("No game logs were extracted")
