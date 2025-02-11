import logging
from typing import Dict, List

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

from nba_data_forge.dashboard.client import DataClient


class Dashboard:
    def __init__(self):
        self.client = DataClient()

    def create_stats_table(self, stats: Dict):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Points", f"{stats["points_per_game"]:.1f}")
            st.metric("Rebounds", f"{stats["rebounds_per_game"]:.1f}")
            st.metric("Assists", f"{stats["assists_per_game"]:.1f}")

        with col2:
            st.metric("Steals", f"{stats["steals_per_game"]:.1f}")
            st.metric("Blocks", f"{stats["blocks_per_game"]:.1f}")

        with col3:
            st.metric("Minutes", f"{stats["minutes_per_game"]:.1f}")
            st.metric("Games Played", f"{stats["games_played"]}")

    def run(self):
        """Main dashboard application."""
        st.title("NBA Data Forge Dashboard 🏀")

        # Sidebar - Player Selection
        st.sidebar.title("Player Selection")
        players = self.client.get_players()
        player_names = [p["name"] for p in players]
        selected_player_name = st.sidebar.selectbox("Select Player", player_names)

        # Get selected player ID
        selected_player = next(p for p in players if p["name"] == selected_player_name)
        player_id = selected_player["player_id"]

        # Season selection
        seasons = list(range(2024, 2003, -1))
        selected_season = st.sidebar.selectbox(
            "Select Season",
            [None] + seasons,
            format_func=lambda x: "All Seasons" if x is None else str(x),
        )

        # Main content
        stats = self.client.get_player_stats(player_id, selected_season)

        # Display player stats
        st.header(f"{selected_player_name}'s Statistics")
        st.subheader(
            "Career Averages"
            if not selected_season
            else f"{selected_season} Season Averages"
        )
        self.create_stats_table(stats["career_stats"])


if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run()
