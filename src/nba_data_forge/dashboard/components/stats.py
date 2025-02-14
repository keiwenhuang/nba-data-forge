from dataclasses import dataclass

import pandas as pd
import streamlit as st


@dataclass
class AverageStats:
    player_id: str
    season: int
    client: "APIClient"
    opponent: str | None = None
    last_n_games: int | None = None
    title: str | None = None

    def render(self):
        display_title = self.title or (
            f"Last {self.last_n_games} Games Average"
            if self.last_n_games
            else "Season Average"
        )
        st.header(display_title)

        response = self.client.get_player_stats(
            player_id=self.player_id,
            season=self.season,
            opponent=self.opponent if self.opponent != "All" else None,
            last_n_games=self.last_n_games if self.last_n_games else None,
        )

        if response and response.get("averages"):
            print(response["averages"])
            stats = pd.DataFrame([response["averages"]])
            st.dataframe(
                stats[
                    [
                        "avg_points",
                        "avg_minutes",
                        "avg_made_field_goals",
                        "avg_attempted_field_goals",
                        "avg_made_threes",
                        "avg_attempted_threes",
                        "avg_made_free_throws",
                        "avg_attempted_free_throws",
                        "avg_offensive_rebounds",
                        "avg_defensive_rebounds",
                        "avg_assists",
                        "avg_steals",
                        "avg_blocks",
                        "avg_turnovers",
                        "avg_fouls",
                        "avg_game_score",
                        "avg_plus_minus",
                    ]
                ],
                hide_index=True,
            )
        else:
            st.info("No stats available for selected filters")


@dataclass
class RecentGameLogs:
    player_id: str
    season: int
    opponent: str | None
    last_n_games: int | None
    client: "APIClient"

    def render(self):
        st.header(f"Last {self.last_n_games} Games Log")

        response = self.client.get_player_stats(
            player_id=self.player_id,
            season=self.season,
            opponent=self.opponent if self.opponent != "All" else None,
            last_n_games=self.last_n_games,
        )

        if response and response.get("games"):
            games = pd.DataFrame(response["games"])
            st.dataframe(
                games[
                    [
                        "date",
                        "team",
                        "opponent",
                        "is_home",
                        "is_win",
                        "minutes_played",
                        "made_field_goals",
                        "attempted_field_goals",
                        "made_three_point_field_goals",
                        "attempted_three_point_field_goals",
                        "made_free_throws",
                        "attempted_free_throws",
                        "points_scored",
                        "offensive_rebounds",
                        "defensive_rebounds",
                        "assists",
                        "steals",
                        "blocks",
                        "turnovers",
                        "personal_fouls",
                        "game_score",
                        "plus_minus",
                    ]
                ],
                hide_index=True,
            )
        else:
            st.info("No recent games available for selected filters")
