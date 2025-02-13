import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from nba_data_forge.api.models.game_log import Base
from nba_data_forge.common.config.config import config


@pytest.fixture(scope="session")
def engine():
    """Create test database engine."""
    return create_engine(config.get_sqlalchemy_url(test=True))


@pytest.fixture(scope="session")
def tables(engine):
    """Create all tables for testing."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine, tables):
    """Creates a new database session for testing."""
    connection = engine.connect()
    transaction = connection.begin()
    TestingSessionLocal = sessionmaker(bind=connection)
    session = TestingSessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
