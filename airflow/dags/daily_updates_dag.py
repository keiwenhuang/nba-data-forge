from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.log.logging_mixin import LoggingMixin
from nba_data_forge.common.utils.paths import paths
from nba_data_forge.etl.extractors.daily_game_log_extractor import DailyGameLogExtractor
from nba_data_forge.etl.loaders.database import DatabaseLoader
from nba_data_forge.etl.transformers.daily_game_log_transformer import (
    DailyGameLogTransformer,
)

log = LoggingMixin().log

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
    schedule="0 18 * * *",  # Changed from schedule_interval to schedule
    start_date=datetime(2025, 2, 5),
    catchup=False,
    tags=["nba", "daily"],
)


def extract_game_logs(**context):
    extractor = DailyGameLogExtractor()
    current_date = context["data_interval_start"]
    yesterday = current_date - timedelta(days=1)

    try:
        start_date = yesterday - timedelta(days=2)
        end_date = yesterday

        games = extractor.extract(start_date=start_date, end_date=end_date)
        if games.empty:
            log.info(f"No games found on {yesterday.date()}")
            return None

        raw_dir = paths.get_path("raw")
        raw_file = raw_dir / f"game_logs_{yesterday.strftime('%Y%m%d')}.csv"
        games.to_csv(raw_file, index=False)

        log.info(f"Extracted {len(games)} game logs")
        context["task_instance"].xcom_push(key="raw_file", value=str(raw_file))
        return len(games)

    except Exception as e:
        log.error(f"Error extracting daily games: {str(e)}")
        raise


def transform_game_logs(**context):
    try:
        raw_file = context["task_instance"].xcom_pull(
            task_ids="extract_games", key="raw_file"
        )
        if not raw_file:
            log.info("No data to transform")
            return None

        raw_df = pd.read_csv(raw_file)
        transformer = DailyGameLogTransformer()
        transformed_df = transformer.transform(raw_df)

        # save transformed data
        processed_dir = paths.get_path("processed")
        transformed_file = processed_dir / f"{Path(raw_file).stem}_transformed.csv"
        transformed_df.to_csv(transformed_file, index=False)

        log.info(f"Transformed {len(transformed_df)} game logs")
        context["task_instance"].xcom_push(
            key="transformed_file", value=str(transformed_file)
        )
        return len(transformed_df)

    except Exception as e:
        log.error(f"Error transforming game logs: {str(e)}")
        raise


def load_game_logs(**context):
    try:
        transformed_file = context["task_instance"].xcom_pull(
            task_ids="transform_games", key="transformed_file"
        )
        if not transformed_file:
            log.info("No data to load")
            return None

        df = pd.read_csv(transformed_file)
        loader = DatabaseLoader()

        # Use upsert to handle potential duplicates
        rows_affected = loader.upsert(
            df,
            table_name="game_logs",
            unique_columns=["date", "player_id", "team"],
        )

        # Get archive directories for raw and transformed files
        raw_archive_dir = paths.get_path("raw_archive")
        transformed_archive_dir = paths.get_path("transformed_archive")

        # Archive raw file
        raw_file = context["task_instance"].xcom_pull(
            task_ids="extract_games", key="raw_file"
        )
        if raw_file:
            source_path = Path(raw_file)
            if source_path.exists():
                archive_path = raw_archive_dir / source_path.name
                source_path.rename(archive_path)
                log.info(f"Archived raw file to {archive_path}")

        # Archive transformed file
        if transformed_file:
            source_path = Path(transformed_file)
            if source_path.exists():
                archive_path = transformed_archive_dir / source_path.name
                source_path.rename(archive_path)
                log.info(f"Archived transformed file to {archive_path}")

        log.info(f"Loaded {rows_affected} games to database")
        return rows_affected

    except Exception as e:
        log.error(f"Error loading game logs: {str(e)}")
        raise


def validate_daily_games(**context):
    """Validate the loaded data."""
    try:
        loader = DatabaseLoader()
        yesterday = context["data_interval_start"].date() - timedelta(days=1)

        # Check for duplicates
        duplicates = loader.check_duplicates(
            table_name="game_logs",
            columns=["date", "player_id", "team"],
            date=yesterday,
        )
        if duplicates:
            log.warning(f"Found {len(duplicates)} duplicate entries")

        # Verify data completeness
        games_count = loader.count_games(date=yesterday)
        expected_count = context["task_instance"].xcom_pull(task_ids="transform_games")

        if games_count != expected_count:
            log.error(
                f"Data mismatch: expected {expected_count} games, found {games_count}"
            )
            raise ValueError("Data validation failed")

        log.info("Data validation successful")
        return True

    except Exception as e:
        log.error(f"Error validating daily games: {str(e)}")
        raise


# define tasks
extract_games = PythonOperator(
    task_id="extract_games", python_callable=extract_game_logs, dag=dag
)

transform_games = PythonOperator(
    task_id="transform_games", python_callable=transform_game_logs, dag=dag
)

load_games = PythonOperator(
    task_id="load_games", python_callable=load_game_logs, dag=dag
)

validate_games = PythonOperator(
    task_id="validate_games", python_callable=validate_daily_games, dag=dag
)

# Set task dependencies
extract_games >> transform_games >> load_games >> validate_games


if __name__ == "__main__":
    dag.test()
