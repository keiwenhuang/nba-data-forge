from sqlalchemy import VARCHAR, Boolean, Column, Date, Integer, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class GameLog(Base):
    __tablename__ = "game_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    team = Column(VARCHAR(30), nullable=False)
    location = Column(VARCHAR(15), nullable=False)
    opponent = Column(VARCHAR(30), nullable=False)
    outcome = Column(VARCHAR(15), nullable=False)
    active = Column(Boolean, nullable=False)
    seconds_played = Column(Integer, nullable=False)
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
    plus_minus = Column(Integer, nullable=False)
    player_id = Column(VARCHAR(20), nullable=False)
    player_name = Column(VARCHAR(50), nullable=False)
    is_home = Column(Boolean, nullable=False)
    is_win = Column(Boolean, nullable=False)
    minutes_played = Column(Numeric(10, 3), nullable=False)
