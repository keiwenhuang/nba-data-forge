from sqlalchemy import (
    VARCHAR,
    Boolean,
    Column,
    Date,
    Index,
    Integer,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class GameLog(Base):
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

    __tablename__ = "game_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # basic game metadata
    date = Column(Date, nullable=False)
    player_id = Column(VARCHAR(20), nullable=False)
    name = Column(VARCHAR(50), nullable=False)
    team = Column(VARCHAR(30), nullable=False)
    opponent = Column(VARCHAR(30), nullable=False)

    # derived columns
    team_abbrev = Column(VARCHAR(3), nullable=False)
    opponent_abbrev = Column(VARCHAR(3), nullable=False)
    is_home = Column(Boolean, nullable=False)
    is_win = Column(Boolean, nullable=False)

    # game details
    location = Column(VARCHAR(15), nullable=False)
    outcome = Column(VARCHAR(15), nullable=False)
    active = Column(Boolean, nullable=False)

    # playing time
    seconds_played = Column(Integer, nullable=False)
    minutes_played = Column(Numeric(10, 3), nullable=False)

    # performance stats
    made_field_goals = Column(Integer, nullable=False)
    attempted_field_goals = Column(Integer, nullable=False)
    made_three_point_field_goals = Column(Integer, nullable=False)
    attempted_three_point_field_goals = Column(Integer, nullable=False)
    made_free_throws = Column(Integer, nullable=False)
    attempted_free_throws = Column(Integer, nullable=False)
    offensive_rebounds = Column(Integer, nullable=False)
    defensive_rebounds = Column(Integer, nullable=False)
    assists = Column(Integer, nullable=False)
    steals = Column(Integer, nullable=False)
    blocks = Column(Integer, nullable=False)
    turnovers = Column(Integer, nullable=False)
    personal_fouls = Column(Integer, nullable=False)
    points_scored = Column(Integer, nullable=False)
    game_score = Column(Numeric(10, 1), nullable=False)
    plus_minus = Column(Numeric(5, 1), nullable=False)  # Updated type
    season = Column(Integer, nullable=False)  # Added season column

    __table_args__ = (
        UniqueConstraint("date", "player_id", "team", name="unique_game_player_team"),
        Index("idx_game_logs_player_id", "player_id"),
        Index("idx_game_logs_date", "date"),
        Index("idx_game_logs_player_date", "player_id", "date"),
    )
