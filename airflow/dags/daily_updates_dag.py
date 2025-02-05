from datetime import datetime, timedelta

import pandas as pd

from airflow import DAG
from airflow.utils.log.logging_mixin import LoggingMixin
from nba_data_forge.etl.extractors.game_log_extractor import GameLogExtractor

log = LoggingMixin().log
tomorrow = datetime.now().date() + timedelta(days=1)

default_args = {
    "owner": "nba_data_forge",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


dag = DAG(
    "nba_daily_updates",
    default_args=default_args,
    description="NBA current season game log updates",
    schedule_interval="0 12 * * *",  # 12 PM UTC (7 AM EST)
    start_date="2025-02-05",
    catchup=False,
    tags=["nba", "daily"],
)


def extract_daily_games(**context):
    extractor = GameLogExtractor()
    execution_date = context["execution_date"]
    yesterday = execution_date - timedelta(days=1)  # Get yesterday's games

    try:
        start_date = yesterday - timedelta(days=2)
        end_date = yesterday

        games = extractor.extract_date_range(start_date, end_date)
        if games.empty:
            log.info(f"No games found on {yesterday.date}")
            return None

        log.info(f"Extracted {len(games)} games")
        return pd.DataFrame(games)

    except Exception as e:
        log.error(f"Error extracting daily games: {str(e)}")
        raise
