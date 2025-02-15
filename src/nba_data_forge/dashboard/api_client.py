from typing import Dict, List

import requests
import streamlit as st


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()

    def get_players(self, season: int) -> List[Dict]:
        try:
            response = self.session.get(
                f"{self.base_url}/players/", params={"season": season}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch players: {str(e)}")
            return []

    def get_team_abbrev(self) -> List[str]:
        """Get list of team abbreviations."""

        response = self.session.get(f"{self.base_url}/teams/abbreviations")
        response.raise_for_status()
        return response.json()

    def get_season_games(
        self,
        player_id: str,
        season: int | None = None,
    ):

        response = self.session.get(
            f"{self.base_url}/players/{player_id}/season/{season}"
        )
        response.raise_for_status()
        return response.json()

    def get_recent_averages(
        self,
        player_id: str,
        opponent_abbrev: str | None = None,
        last_n_games: int | None = None,
    ):
        params = {}

        if opponent_abbrev:
            params["opponent_abbrev"] = opponent_abbrev
        if last_n_games:
            params["last_n_games"] = last_n_games

        response = self.session.get(
            f"{self.base_url}/players/{player_id}/vs-opponent-stats", params=params
        )
        response.raise_for_status()
        return response.json()
