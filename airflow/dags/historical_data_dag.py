"""NBA Historical Game Logs ETL Pipeline DAG

This DAG implements a parallel processing pipeline for historical NBA game log data,
processing multiple seasons concurrently. Each season goes through extract, transform,
and load stages, with data quality checks and metrics tracking at each stage.

The pipeline processes seasons from 2004 to 2024, with a concurrency limit of 4 seasons
to balance performance with system resources.

Flow:
    start_pipeline 
        -> extract_{season} 
        -> transform_{season} 
        -> load_{season} 
    -> end_pipeline

Key Features:
    - Parallel processing of seasons (max 4 concurrent)
    - Error handling and retries
    - Metrics tracking via XCom
    - Intermediate file storage in temp directory
"""

from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from airflow import DAG
from airflow.models import TaskInstance
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.log.logging_mixin import LoggingMixin
from nba_data_forge.common.utils.paths import paths
from nba_data_forge.etl.loaders.database import DatabaseLoader
from nba_data_forge.etl.transformers.game_log_transformer import GameLogTransformer

default_args = {
    "owner": "nba_data_forge",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

log = LoggingMixin().log


def get_season_file_path(season: int, stage: str = "raw") -> Path:
    """
    Construct the file path for a given season's data file.

    Args:
        season: NBA season year (e.g., 2024 for 2023-24 season)
        stage: Processing stage ('raw' or 'transformed')

    Returns:
        Path object pointing to the season's data file
    """
    file_mapping = {
        "raw": f"game_logs_{season}.csv",
        "transformed": f"game_logs_{season}_transformed.csv",
    }
    return paths.get_path(stage) / file_mapping[stage]


def extract_season_data(season: int, ti: TaskInstance) -> None:
    """Extract game log data for a specific season.

    Reads the raw CSV file for the season, adds a season column,
    and saves to temporary storage for transformation.

    Args:
        season: NBA season year
        ti: Airflow task instance for XCom pushing

    Raises:
        FileNotFoundError: If season's raw data file doesn't exist
        Exception: For other processing errors
    """
    log.info(f"Starting extraction for season {season}")

    try:
        season_file = get_season_file_path(season, "raw")
        if not season_file.exists():
            raise FileNotFoundError(f"No data file found for season {season}")

        df = pd.read_csv(season_file)

        # add season column and save to temp
        df["season"] = season
        temp_file = paths.get_path("temp") / f"game_logs_{season}.csv"
        df.to_csv(temp_file, index=False)

        # Push metrics to XCom
        metrics = {"record_count": len(df)}
        ti.xcom_push(key=f"extract_metrics_{season}", value=metrics)

        log.info(f"Successfully extracted {len(df)} records for season {season}")
    except Exception as e:
        log.error(f"Error extracting season {season}: {str(e)}")
        ti.xcom_push(key=f"extract_error_{season}", value=str(e))
        raise


def transform_season_data(season: int, ti: TaskInstance) -> None:
    """Transform extracted game log data.

    Applies transformations including:
    - Team name standardization
    - Boolean flag creation
    - Statistical calculations

    Args:
        season: NBA season year
        ti: Airflow task instance for XCom pushing

    Raises:
        Exception: For any transformation errors
    """
    log.info(f"Starting transformation for season {season}")

    try:
        # read extracted data
        input_path = paths.get_path("temp") / f"game_logs_{season}.csv"
        raw_data = pd.read_csv(input_path)

        # transform data
        transformer = GameLogTransformer()
        transformed_data = transformer.transform(raw_data)

        # save transformed data
        output_path = paths.get_path("temp") / f"game_logs_{season}_transformed.csv"
        transformed_data.to_csv(output_path, index=False)

        # Push metrics to XCom
        metrics = {"record_count": len(transformed_data)}
        ti.xcom_push(key=f"transform_metrics_{season}", value=metrics)

        log.info(
            f"Successfully transformed {len(transformed_data)} records for season {season}"
        )

    except Exception as e:
        log.error(f"Error transforming season {season}: {str(e)}")
        ti.xcom_push(key=f"transform_error_{season}", value=str(e))
        raise


def load_season_data(season: int, ti: TaskInstance) -> None:
    """Load transformed season data into the database.

    Performs data quality checks before loading and tracks
    loading metrics via XCom.

    Args:
        season: NBA season year
        ti: Airflow task instance for XCom pushing

    Raises:
        FileNotFoundError: If transformed data file is missing
        ValueError: If data is empty
        Exception: For database loading errors
    """
    log.info(f"Starting database load for season {season}")

    try:
        # read transform data
        input_path = paths.get_path("temp") / f"game_logs_{season}_transformed.csv"

        if not input_path.exists():
            raise FileNotFoundError(f"No transformed data file found at {input_path}")

        data = pd.read_csv(input_path)

        log.info(f"Read {len(data)} records from {input_path}")

        if data.empty:
            raise ValueError(f"Empty dataframe loaded from {input_path}")

        # load data
        loader = DatabaseLoader()
        loader.load(data)

        # push metrics to XCom
        metrics = {"records_loaded": len(data)}
        ti.xcom_push(key=f"load_metrics_{season}", value=metrics)

        log.info(f"Successfully loaded {len(data)} records for season {season}")

    except Exception as e:
        log.error(f"Error loading season {season}: {str(e)}")
        ti.xcom_push(key=f"load_error_{season}", value=str(e))
        raise


with DAG(
    "nba_historical_data_parallel",
    default_args=default_args,
    description="Parallel ETL processing for NBA game logs by season",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["nba", "historical", "game_logs"],
    concurrency=4,  # Process 4 seasons simultaneously
) as tag:

    # pipeline start and end markers
    start_pipeline = EmptyOperator(task_id="start_pipeline")
    end_pipeline = EmptyOperator(task_id="end_pipeline")

    # create task for each season
    for season in range(2004, 2025):  # up to 2024 season
        extract_task = PythonOperator(
            task_id=f"extract_{season}",
            python_callable=extract_season_data,
            op_kwargs={"season": season},
            provide_context=True,
        )

        transform_task = PythonOperator(
            task_id=f"transform_{season}",
            python_callable=transform_season_data,
            op_kwargs={"season": season},
            provide_context=True,
        )

        load_task = PythonOperator(
            task_id=f"load_{season}",
            python_callable=load_season_data,
            op_kwargs={"season": season},
            provide_context=True,
        )

        # set up dependencies for this season
        start_pipeline >> extract_task >> transform_task >> load_task >> end_pipeline
