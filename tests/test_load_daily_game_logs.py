import pandas as pd
from sqlalchemy import create_engine, text

from nba_data_forge.common.config.config import config
from nba_data_forge.common.utils.paths import paths
from nba_data_forge.etl.loaders.database import DatabaseLoader
from nba_data_forge.etl.transformers.daily_game_log_transformer import (
    DailyGameLogTransformer,
)


def check_table_counts():
    """Check row counts for all tables in the database."""
    try:
        # Create database connection
        engine = create_engine(config.get_database_url(test=True))

        # Get list of tables and their row counts
        query = """SELECT COUNT(*) FROM game_logs;"""

        with engine.begin() as connection:
            result = connection.execute(text(query))
            row_count = result.scalar()
            print(f"Row count: {row_count}")

    except Exception as e:
        print(f"Error checking table counts: {str(e)}")
        raise


unique_columns = ["date", "player_id", "team"]


sample = pd.read_csv(paths.get_path("sample") / "sample_daily.csv")
transformer = DailyGameLogTransformer()
transformed_sample = transformer.transform(sample)

print("Before loading data....")
check_table_counts()

loader = DatabaseLoader(test=True)
loader.upsert(
    df=transformed_sample, table_name="game_logs", unique_columns=unique_columns
)
loader.check_duplicates(table_name="game_logs", columns=unique_columns)
print(loader.count_games("2024-02-01"))
# loader.load(transformed_sample)

print("After loading data....")
check_table_counts()
