from datetime import date

from pydantic import BaseModel


class GameLog(BaseModel):
    date: date
    team: str
    opponent: str
    is_win: bool
    is_home: bool
