import streamlit as st

from nba_data_forge.dashboard.api_client import APIClient
from nba_data_forge.dashboard.components.filters import (
    LastNGamesFilter,
    OpponentFilter,
    PlayerFilter,
    SeasonFilter,
)
from nba_data_forge.dashboard.components.stats import AverageStats, RecentGameLogs


def main():
    st.set_page_config(page_title="NBA Stats Dashboard", page_icon="🏀", layout="wide")

    st.title("NBA Player Statistics Dashboard")
    client = APIClient()

    with st.sidebar:
        st.header("Filters")
        with st.spinner("Loading filters..."):
            season = SeasonFilter().render()
            player = PlayerFilter(season=season, client=client).render()
            opponent = OpponentFilter(client=client).render()
            last_n_games = LastNGamesFilter(client=client).render()

    if player:
        row1, row2, row3 = st.container(), st.container(), st.container()

        # Season averages
        with row1:
            AverageStats(
                player_id=player,
                season=season,
                client=client,
            ).render()

        # Last N games averages
        with row2:
            AverageStats(
                player_id=player,
                season=season,
                opponent=opponent,
                last_n_games=last_n_games,
                client=client,
            ).render()

        with row3:
            RecentGameLogs(
                player_id=player,
                season=season,
                opponent=opponent,
                last_n_games=last_n_games,
                client=client,
            ).render()


if __name__ == "__main__":
    main()
