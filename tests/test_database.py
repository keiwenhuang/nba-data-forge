from airflow.utils.log.logging_mixin import LoggingMixin
from nba_data_forge.etl.loaders.database import DatabaseLoader


def test_database_connection():
    logger = LoggingMixin().log
    try:
        loader = DatabaseLoader()

        with loader.engine.connect() as connection:
            logger.info("Successfully connected to database")

        loader._create_table()
        logger.info("Successfully created tables")

        return True

    except Exception as e:
        logger.error(f"Database test failed: {str(e)}")


if __name__ == "__main__":
    test_database_connection()
