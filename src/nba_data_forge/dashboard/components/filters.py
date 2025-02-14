from dataclasses import dataclass

import streamlit as st


@dataclass
class SeasonFilter:
    def render(self) -> int:
        return st.selectbox(
            "Season", range(2025, 2004, -1), format_func=lambda x: f"{x-1}-{x}"
        )


@dataclass
class PlayerFilter:
    season: int
    client: "APIClient"

    def render(self) -> str | None:
        players = self.client.get_players(self.season)
        options = {p["name"]: p["player_id"] for p in players}

        selected_name = st.selectbox("Player", options=list(options.keys()))

        return options.get(selected_name)


@dataclass
class OpponentFilter:
    client: "APIClient"

    def render(self) -> str | None:
        teams = self.client.get_team_abbrev()
        return st.selectbox(
            "Opponent",
            options=["All"] + teams,
            format_func=lambda x: "All Teams" if x == "All" else x,
        )


@dataclass
class LastNGamesFilter:
    client: "APIClient"

    def render(self) -> str | None:
        return st.selectbox("Last N Games", range(3, 82, 5))
