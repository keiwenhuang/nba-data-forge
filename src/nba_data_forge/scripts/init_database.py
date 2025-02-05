from sqlalchemy import create_engine, text

from nba_data_forge.common.config.config import config
from nba_data_forge.common.utils.logger import setup_logger
from nba_data_forge.common.utils.path import get_project_root


def init_database():
    logger = setup_logger(__file__, get_project_root() / "logs")
    engine = create_engine(config.get_sqlalchemy_url())
    logger.info("Initializing database schema...")

    sql_file = get_project_root() / "src/nba_data_forge/scripts/sql/create_table.sql"

    try:
        with engine.begin() as conn:
            conn.execute(text(sql_file.read_text()))
        logger.info("Database schema initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise


if __name__ == "__main__":
    init_database()
