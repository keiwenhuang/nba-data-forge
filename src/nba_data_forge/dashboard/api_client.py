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

    def get_player_stats(
        self,
        player_id: str,
        season: int | None = None,
        opponent: str | None = None,
        last_n_games: int | None = None,
    ):
        params = {"season": season}

        if opponent:
            params["opponent"] = opponent
        if last_n_games:
            params["last_n_games"] = last_n_games

        response = self.session.get(
            f"{self.base_url}/players/{player_id}/games", params=params
        )
        response.raise_for_status()
        return response.json()

    def get_team_abbrev(self) -> List[str]:
        """Get list of team abbreviations."""

        response = self.session.get(f"{self.base_url}/teams/abbreviations")
        response.raise_for_status()
        return response.json()
