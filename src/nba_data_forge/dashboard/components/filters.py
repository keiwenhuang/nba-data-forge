from dataclasses import dataclass

import streamlit as st


@dataclass
class BaseFilter:
    """Base class for filters with common functionality"""

    client: "APIClient"

    def handle_error(self, message: str) -> None:
        st.error(f"Error in filter: {message}")


@dataclass
class SeasonFilter:

    def render(self) -> int:
        return st.selectbox(
            "Season", range(2025, 2004, -1), format_func=lambda x: f"{x-1}-{x}"
        )


@dataclass
class LastNGamesFilter:

    def render(self) -> int | None:
        return st.selectbox("Last N Games", range(3, 82, 5))


@dataclass
class PlayerFilter(BaseFilter):
    season: int

    def render(self) -> str | None:
        try:
            players = self.client.get_players(self.season)
            options = {p["name"]: p["player_id"] for p in players}

            selected_name = st.selectbox("Player", options=list(options.keys()))

            return options.get(selected_name)
        except Exception as e:
            self.handle_error(str(e))
            return None


@dataclass
class OpponentFilter(BaseFilter):

    def render(self) -> str | None:
        try:
            teams = self.client.get_team_abbrev()
            return st.selectbox(
                "Opponent",
                options=["All"] + teams,
                format_func=lambda x: "All Teams" if x == "All" else x,
            )
        except Exception as e:
            self.handle_error(str(e))
