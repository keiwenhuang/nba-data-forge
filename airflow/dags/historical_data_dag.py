from datetime import datetime, timedelta

import pandas as pd

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.task_group import TaskGroup
from nba_data_forge.common.config.paths import paths
from nba_data_forge.etl.loaders.database import DatabaseLoader
from nba_data_forge.etl.transformers.game_log_transformer import GameLogTransformer

default_args = {
    "owner": "nba_data_forge",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def combine_historical_data(**context):
    data_dir = paths.get_path("raw")

    logger = LoggingMixin().log
    logger.info(f"Starting historical data combination from: {data_dir}")
    logger.info(f"Directory exists: {data_dir.exists()}")

    all_game_logs = []
    season_files = data_dir.glob("game_logs_*.csv")
    for season_file in season_files:
        try:
            df = pd.read_csv(season_file)
            df["season"] = int(
                season_file.stem.split("_")[2]
            )  # Extract year from filename
            all_game_logs.append(df)
            logger.info(f"Processed {season_file.name}: {len(df)} records")
        except Exception as e:
            logger.error(f"Error processing {season_file.name}: {str(e)}")

    combined_data = pd.concat(all_game_logs, ignore_index=True)

    # validation
    season_counts = combined_data.groupby("season").size()
    context["task_instance"].xcom_push(
        key="season_counts", value=season_counts.to_dict()
    )

    output_path = paths.get_path("temp") / "historical_game_logs_raw.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined_data.to_csv(output_path, index=False)
    return f"Combined {len(all_game_logs)} season files, Total record: {len(combined_data)}"


def transform_data(**context):
    logger = LoggingMixin().log

    transformer = GameLogTransformer()
    temp_dir = paths.get_path("temp")
    input_path = temp_dir / "historical_game_logs_raw.csv"

    raw_data = pd.read_csv(input_path)
    transformed_data = transformer.transform(raw_data)
    output_path = temp_dir / "historical_game_logs_transformed.csv"
    transformed_data.to_csv(output_path, index=False)

    summary = {
        "total record": len(transformed_data),
        "seasons": transformed_data["season"].nunique(),
        "players": transformed_data["player_id"].nunique(),
        "team": transformed_data["team"].nunique(),
    }

    context["task_instance"].xcom_push(key="transformation_summary", value=summary)
    logger.info(f"Transformation summary: {summary}")
    return f"Tranformed {summary['total record']} records across {summary['seasons']} seasons"


def load_data(**context):
    loader = DatabaseLoader()
    input_path = paths.get_path("temp") / "historical_game_logs_transformed.csv"
    data = pd.read_csv(input_path)
    loader.load(data)

    summary = {"record_loaded": len(data), "load_timestamp": datetime.now().isoformat()}
    context["task_instance"].xcom_push(key="load_summery", value=summary)
    return f"Loaded {summary['record_loaded']} records to database"


with DAG(
    "nba_historical_data",
    default_args=default_args,
    description="Load historical NBA game log data",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["nba", "historical", "game_logs"],
) as tag:

    start_pipeline = EmptyOperator(task_id="start_pipeline")

    with TaskGroup("data_processing") as processing_group:
        combined_data = PythonOperator(
            task_id="combine_historical_data", python_callable=combine_historical_data
        )

        transform = PythonOperator(
            task_id="transform_data", python_callable=transform_data
        )

        load = PythonOperator(task_id="load_data", python_callable=load_data)

        combined_data >> transform >> load

    end_pipeline = EmptyOperator(task_id="end_pipeline")

    start_pipeline >> processing_group >> end_pipeline
