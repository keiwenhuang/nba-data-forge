from typing import List

import pandas as pd
from sqlalchemy import create_engine, text

from nba_data_forge.common.config.config import config
from nba_data_forge.common.utils.logger import setup_logger
from nba_data_forge.common.utils.paths import paths


class DatabaseLoader:
    """Handles loading of transformed NBA game log data into PostgreSQL database.

    This class assumes the database and required tables have already been created
    through the database initialization script. It focuses solely on efficient
    data loading using SQLAlchemy and pandas.

    Attributes:
        logger: Configured logger for the database loading operations
        engine: SQLAlchemy engine instance for database connections

    Note:
        Before using this loader, ensure that:
        1. The database has been created
        2. The schema has been initialized using init_database.py script
        3. The game_logs table exists with the correct structure
    """

    def __init__(self, test: bool = False):
        """Initialize DatabaseLoader with optional test mode.

        Args:
            test: If True, uses test database configuration
        """
        self.logger = setup_logger(__class__.__name__, paths.get_path("logs"))
        self.engine = create_engine(config.get_sqlalchemy_url(test))

    def load(self, df: pd.DataFrame):
        """Load transformed game log data into the database.

        Uses pandas to_sql with optimized parameters for bulk loading:
        - method='multi' for faster inserts
        - chunksize=10000 to handle large datasets efficiently
        - if_exists='append' to add new records to existing table

        Args:
            df: pandas DataFrame containing transformed game log data.
                Expected to match the game_logs table schema.

        Raises:
            Exception: If any database operation fails, with error details logged.

        Example:
            loader = DatabaseLoader()
            loader.load(transformed_game_logs_df)
        """
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

    def upsert(
        self, df: pd.DataFrame, table_name: str, unique_columns: List[str]
    ) -> int:
        try:
            temp_table = f"temp_{table_name}"

            # create temporary table with same main table structure
            create_temp_sql = f"""
                CREATE TEMP TABLE {temp_table} (LIKE {table_name} INCLUDING ALL)
                ON COMMIT DROP
            """
            self.logger.info(f"{temp_table} created...")

            with self.engine.begin() as conn:
                conn.execute(text(create_temp_sql))
                df.to_sql(
                    temp_table,
                    conn,
                    if_exists="append",
                    index=False,
                    method="multi",
                )
                self.logger.info(f"Data loaded to {temp_table} successfully")

                unique_cols_str = ", ".join(unique_columns)
                update_cols = [col for col in df.columns if col not in unique_columns]
                set_clause = ", ".join(f"{col} = EXCLUDED.{col}" for col in update_cols)

                # perform upsert
                upsert_sql = f"""
                    INSERT INTO {table_name}
                    SELECT * FROM {temp_table}
                    ON CONFLICT ({unique_cols_str})
                    DO UPDATE SET {set_clause}            
                """

                result = conn.execute(text(upsert_sql))

            row_affected = result.rowcount
            self.logger.info(f"Upserted {row_affected} rows")
            return row_affected

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
