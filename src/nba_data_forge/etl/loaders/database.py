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

    def __init__(self, test=False):
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
