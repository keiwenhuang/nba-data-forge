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
                self.logger.info(f"Fetching game logs for date {date}")

                logs = client.player_box_scores(
                    day=date.day, month=date.month, year=date.year
                )

                self.logger.info(f"Successfully fetched {len(logs)} games")
                return logs
            except Exception as e:
                if attempt == self.max_retries - 1:
                    self.logger.error(
                        f"Failed all {self.max_retries} attempts: {str(e)}"
                    )
                    raise

                self.logger.warning(
                    f"Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}. Retrying..."
                )
                self._api_delay((5, 15))

    def extract_daily(self, target_date: date) -> pd.DataFrame:
        # extracting two days range of data to catch missed or updated data
        start_date = target_date - timedelta(days=1)
        end_date = target_date

        return self.extract(start_date, end_date)

    def extract(self, start_date: date, end_date: date):
        self.logger.info(f"Extracting game logs from {start_date} to {end_date}")

        # Load global progress
        all_games = []

        current = start_date
        while current <= end_date:
            try:
                self.logger.info(f"Processing data: {current}")
                daily_games = self._get_game_logs_by_date(current)

                if daily_games:
                    for game in daily_games:
                        game["date"] = current
                    all_games.extend(daily_games)

                    self.logger.info(
                        f"Successfully processed {current}: {len(daily_games)}"
                    )
            except Exception as e:
                self.logger.error(f"Error to process {current}: {str(e)}")
                raise

            current += timedelta(days=1)

        if not all_games:
            self.logger.info("No new games found in date range")
            return pd.DataFrame()

        return pd.DataFrame(all_games)

    def validate(self, df):
        return super().validate(df)
