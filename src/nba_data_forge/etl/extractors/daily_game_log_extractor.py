from datetime import date, timedelta

import pandas as pd
from basketball_reference_web_scraper import client

from nba_data_forge.etl.extractors.base import BaseExtractor


class DailyGameLogExtractor(BaseExtractor):
    def __init__(self, max_retries=3):
        super().__init__()
        self.max_retries = max_retries

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

    def extract(self, start_date: date, end_date: date):
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
