from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from nba_data_forge.common.config import config

DATABASE_URL = config.get_database_url()
engine = create_engine(url=DATABASE_URL)
Session = sessionmaker(engine)
Base = declarative_base()


def get_session():
    with Session() as session:
        yield session
