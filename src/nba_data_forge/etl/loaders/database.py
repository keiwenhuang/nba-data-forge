"""
Database handling module for NBA game log data.

This module provides functionality to:
- Connect to PostgreSQL database
- Create/update tables
- Load game log data using temporary tables and upsert
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from nba_data_forge.common.config.config import config
from nba_data_forge.common.utils.path import get_project_root


class DatabaseLoader:
    """Handles database operations for NBA game log data"""

    def __init__(self, create_db):
        """
        Args:
            create_db (bool): If true, creates database if not exists
        """
        # if create_db:
        #     self._create_database()

        self.engine = self._create_engine()
        self.sql_dir = get_project_root() / "src/nba_data_forge/etl/loaders/sql"

    def _create_engine(self):
        """Create SQLAlchemy engine using config"""
        try:
            db_url = config.get_database_url()
            return create_engine(db_url)

        except Exception as e:
            raise Exception(f"Failed to create database engine: {e}")

    def _load_sql(self, file_name):
        """Load SQL query from file"""
        sql_path = Path(self.sql_dir / file_name)
        return sql_path.read_text()

    def _create_table(self):
        """Create game_logs table if does not exist"""
        create_table_sql = self._load_sql("create_tables.sql")
        with self.engine.begin() as connection:
            connection.execute(text(create_table_sql))

    def load(self, df: pd.DataFrame):
        """Load game log data using upsert pattern

        Args:
            df (pd.DataFrame): contains game log data

        Process:
        1. Ensure table exists
        2. Load data to temporary table
        3. Upsert from temporary to main table
        4. Clean up temporary table
        """
        try:
            self._create_table()
            df.to_sql("temp_game_logs", self.engine, if_exists="replace", index=False)

            upsert_sql = self._load_sql("upsert_game_logs.sql")
            with self.engine.begin() as connection:
                connection.execute(text(upsert_sql))
                connection.execute(text("DROP TABLE IF EXISTS temp_game_logs;"))

            print(f"Successfully loaded {len(df)} records")
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise
