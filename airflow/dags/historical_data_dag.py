from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

# from data_engineering.loaders.database import DatabaseLoader
# from data_engineering.transformers.game_log_transformer import GameLogTransformer
# from data_engineering.utils.path import get_project_root

# ROOT = get_project_root()


# Simplified transformer logic
def transform_game_logs(df):
    """Basic transformations without external dependencies"""
    transformed = df.copy()

    # Basic transformations
    transformed["is_home"] = transformed["location"].str.contains("HOME", case=True)
    transformed["is_win"] = transformed["outcome"].str.contains("WIN", case=True)
    transformed["minutes_played"] = transformed["seconds_played"] / 60

    return transformed


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
    # data_dir = Path(ROOT / "data/raw")
    data_dir = Path("/opt/airflow/data/raw")
    print(f"Looking for files in: {data_dir}")
    print(f"Directory exists: {data_dir.exists()}")
    all_game_logs = []

    for season_file in data_dir.glob("sample_game_logs_*.csv"):
        try:
            print(f"Attempting to read: {season_file}")
            df = pd.read_csv(season_file)
            df["season"] = int(
                season_file.stem.split("_")[2]
            )  # Extract year from filename
            all_game_logs.append(df)
            msg = f"Processed {season_file.name}: {len(df)} records"
            print(msg)
            context["task_instance"].xcom_push(
                key=f"processed_file_{season_file.stem}",
                value=f"Processed {season_file.name}: {len(df)} records",
            )
        except Exception as e:
            context["task_instance"].xcom_push(
                key=f"erroe_file_{season_file.stem}",
                value=f"Error processing {season_file.name}: {str(e)}",
            )
            raise

    combined_data = pd.concat(all_game_logs, ignore_index=True)

    # validation
    season_counts = combined_data.groupby("season").size()
    context["task_instance"].xcom_push(
        key="season_counts", value=season_counts.to_dict()
    )

    # output_path = Path(ROOT / "data/temp/historical_game_logs_raw.csv")
    output_path = Path("/opt/airflow/data/temp/historical_game_logs_raw.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined_data.to_csv(output_path, index=False)
    return f"Combined {len(all_game_logs)} season files, Total record: {len(combined_data)}"


def transform_data(**context):
    # transformer = GameLogTransformer()
    # input_path = Path(ROOT / "data/temp/historical_game_logs_raw.csv")
    input_path = Path("/opt/airflow/data/temp/historical_game_logs_raw.csv")

    raw_data = pd.read_csv(input_path)
    # transformed_data = transformer.transform(raw_data)
    transformed_data = transform_game_logs(raw_data)
    # output_path = Path(ROOT / "data/temp/historical_game_logs_transformed.csv")
    output_path = Path("/opt/airflow/data/temp/historical_game_logs_transformed.csv")
    transformed_data.to_csv(output_path, index=False)

    summary = {
        "total record": len(transformed_data),
        "seasons": transformed_data["season"].nunique(),
        "players": transformed_data["player_id"].nunique(),
        "team": transformed_data["team"].nunique(),
    }

    context["task_instance"].xcom_push(key="transformation_summary", value=summary)

    return f"Tranformed {summary['total record']} records across {summary['seasons']} seasons"


def load_data(**context):
    # loader = DatabaseLoader()
    # input_path = Path(ROOT / "data/temp/historical_game_logs_transformed.csv")
    # input_path = Path("/opt/airflow/data/temp/historical_game_logs_transformed.csv")
    # data = pd.read_csv(input_path)
    # loader.load(data)

    # for testing
    input_path = Path("/opt/airflow/data/temp/historical_game_logs_transformed.csv")
    data = pd.read_csv(input_path)
    output_path = Path("/opt/airflow/data/processed/historical_game_logs_final.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)

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
