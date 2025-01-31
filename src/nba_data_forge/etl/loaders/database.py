from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from nba_data_forge.common.config import config
from nba_data_forge.common.utils.path import get_project_root


class DatabaseLoader:
    def __init__(self):
        self.engine = self._create_engine()
        self.sql_dir = get_project_root() / "src/nba_data_forge/etl/loaders/sql"

    def _create_engine(self):
        try:
            db_url = config.get_database_url()
            return create_engine(db_url)

        except Exception as e:
            raise Exception(f"Failed to create database engine: {e}")

    def _load_sql(self, file_name):
        sql_path = Path(self.sql_dir / file_name)
        return sql_path.read_text()

    def _create_table(self):
        create_table_sql = self._load_sql("create_tables.sql")
        with self.engine.connect() as connection:
            connection.execute(text(create_table_sql))
            connection.commit()

    def load(self, df: pd.DataFrame):
        try:
            self._create_table()

            df.to_sql("temp_game_logs", self.engine, if_exists="replace", index=False)

            upsert_sql = self._load_sql("upsert_game_logs.sql")
            with self.engine.connect() as connection:
                connection.execute(text(upsert_sql))

                # Clean up temporary table
                connection.execute(text("DROP TABLE IF EXISTS temp_game_logs;"))
                connection.commit()

            print(f"Successfully loaded {len(df)} records")
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise
