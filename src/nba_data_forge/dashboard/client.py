import requests


class DataClient:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()

    def get_players(self):
        response = self.session.get(f"{self.base_url}/players")
        response.raise_for_status()
        return response.json()["items"]

    def get_player_stats(self, player_id: str, season: int | None = None):
        url = f"{self.base_url}/players/{player_id}"
        if season:
            url += f"?season={season}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
