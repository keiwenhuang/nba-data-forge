from data_engineering.extractors.base import BaseExtractor


class GameLogExtractor(BaseExtractor):
    def extract(self, player_id: str, from_season, to_season):
        data = []
