from typing import List

from sqlalchemy.orm import Session


class TeamService:
    def __init__(self, db: Session):
        self.db = db

    def get_team_abbreviations(self) -> List[str]:
        result = self.db.execute(
            """
            SELECT DISTINCT team_abbrev FROM game_logs
            """
        )

        return [row[0] for row in result]
