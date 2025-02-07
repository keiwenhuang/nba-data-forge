from dataclasses import dataclass
from typing import List

import pandas as pd
from sqlalchemy import create_engine, text

from nba_data_forge.common.config.config import config
from nba_data_forge.common.utils.logger import setup_logger
from nba_data_forge.common.utils.paths import paths


class DatabaseLoader:
    """Handles loading and upserting of NBA game log data into PostgreSQL."""

    def __init__(self, test: bool = False):
        """Initialize DatabaseLoader with database connection."""
        self.logger = setup_logger(__class__.__name__, paths.get_path("logs"))
        self.engine = create_engine(config.get_sqlalchemy_url(test))

    def load(self, df: pd.DataFrame):
        """Efficiently loads game log data into the database using bulk insert."""
        try:
            self.logger.info("Loading to game_logs table...")
            df.to_sql(
                "game_logs",
                self.engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=10000,
            )
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise

    def upsert(self, df: pd.DataFrame, table_name: str, unique_columns: List[str]):
        """Performs an upsert operation (INSERT ON CONFLICT UPDATE) on PostgreSQL."""
        try:
            # create temp table
            temp_table = f"temp_{table_name}"
            create_temp_sql = f"""
                CREATE TEMP TABLE {temp_table} (LIKE {table_name} INCLUDING ALL)
                ON COMMIT DROP;
            """

            with self.engine.begin() as conn:
                # create temp table
                conn.execute(text(create_temp_sql))

                # load data into temp table
                df.to_sql(
                    temp_table, conn, if_exists="append", index=False, method="multi"
                )

                # generate upsert
                unique_cols_str = ",".join(unique_columns)
                update_cols = [col for col in df.columns if col not in unique_columns]
                set_clause = ", ".join(f"{col} = EXCLUDED.{col}" for col in update_cols)

                # perform upsert from temp table
                upsert_sql = f"""
                    INSERT INTO {table_name}
                    SELECT * FROM {temp_table}
                    ON CONFLICT ({unique_cols_str})
                    DO UPDATE SET {set_clause}
                """

                result = conn.execute(text(upsert_sql))

            self.logger.info(f"Upserted {result.rowcount} records into {table_name}")
            return result.rowcount

        except Exception as e:
            self.logger.error(f"Error during upset: {str(e)}")

    def check_duplicates(
        self, table_name: str, columns: List[str], date: str | None = None
    ) -> pd.DataFrame | None:
        try:
            cols_str = ", ".join(columns)
            base_query = f"""
                SELECT {cols_str}, COUNT(*) as duplicate_count
                FROM {table_name}
            """

            # Add date filter only if date is provided
            where_clause = " WHERE DATE(date) = DATE(:date)" if date else ""
            query = f"""
                {base_query}
                {where_clause}
                GROUP BY {cols_str}
                HAVING COUNT(*) > 1
            """

            with self.engine.begin() as conn:
                params = {"date": date} if date else {}
                duplicates = pd.read_sql(text(query), conn, params=params)

            if not duplicates.empty:
                self.logger.warning(
                    f"Found {len(duplicates)} sets of duplicates. "
                    f"Total duplicate records: {duplicates['duplicate_count'].sum() - len(duplicates)}"
                )
                return duplicates
            return None

        except Exception as e:
            self.logger.error(f"Error checking duplicates: {str(e)}")
            raise

    def count_games(self, date: str) -> int:
        """Counts the number of distinct players with games on a specific date."""
        try:
            query = """
                SELECT COUNT(DISTINCT player_id)
                FROM game_logs
                WHERE DATE(date) = DATE(:date)
            """

            with self.engine.begin() as conn:
                result = conn.execute(text(query), {"date": date}).scalar()

            return result or 0

        except Exception as e:
            self.logger.error(f"Error counting games: {str(e)}")
            raise
