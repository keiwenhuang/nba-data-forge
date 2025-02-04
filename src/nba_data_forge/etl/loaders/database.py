"""Database loader for NBA game logs.

Handles PostgreSQL connections, table creation, and data loading with 
transaction safety and error handling.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from nba_data_forge.common.config.config import config
from nba_data_forge.common.utils.logger import setup_logger
from nba_data_forge.common.utils.path import get_project_root


class DatabaseLoader:
    def __init__(self):
        log_dir = get_project_root() / "logs"
        self.logger = setup_logger(__class__.__name__, log_dir=log_dir)

        db_url = config.get_sqlalchemy_url()
        self.engine = create_engine(db_url)
        self.sql_dir = get_project_root() / "src/nba_data_forge/etl/loaders/sql"

    def _load_sql(self, file_name):
        """Load SQL query from file"""
        sql_path = Path(self.sql_dir / file_name)
        return sql_path.read_text()

    def _create_table(self):
        """Create game_logs table if does not exist"""
        create_table_sql = self._load_sql("create_tables.sql")
        try:
            with self.engine.begin() as connection:
                connection.execute(text(create_table_sql))
        except Exception as e:
            self.logger.error(f"Error creating table: {str(e)}")
            raise

    def load(self, df: pd.DataFrame):
        """Load data with upsert pattern using temp table"""
        try:
            self.logger.info(f"Starting data load for temp_game_logs")
            self.logger.info(f"Creating/validating table structure")
            self._create_table()

            self.logger.info(f"Loading {len(df)} records into temporary table")
            df.to_sql(
                "temp_game_logs",
                self.engine,
                if_exists="append",
                index=False,
                method="multi",  # For better performance
                chunksize=10000,  # Handle large datasets
            )

            self.logger.info("Executing upsert and dropping temporary table")
            upsert_and_drop_sql = f"{self._load_sql('upsert_game_logs.sql')}"
            with self.engine.connect() as conn:
                conn.execute(text(upsert_and_drop_sql))
                conn.execute(text("DROP TABLE IF EXISTS temp_game_logs;"))

            self.logger.info(f"Successfully loaded {len(df)} records")
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise
