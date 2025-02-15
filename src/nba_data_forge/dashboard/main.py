import streamlit as st

from nba_data_forge.dashboard.api_client import APIClient
from nba_data_forge.dashboard.components.filters import (
    LastNGamesFilter,
    OpponentFilter,
    PlayerFilter,
    SeasonFilter,
)
from nba_data_forge.dashboard.components.stats import (
    RecentGameLogs,
    RecentGameStats,
    SeasonAverage,
)


def main():
    st.set_page_config(page_title="NBA Data Forge", page_icon="🏀", layout="wide")

    st.title("NBA Data Forge Dashboard")
    client = APIClient()

    with st.sidebar:
        st.header("Filters")
        with st.spinner("Loading filters..."):
            season = SeasonFilter().render()
            player = PlayerFilter(season=season, client=client).render()
            opponent_abbrev = OpponentFilter(client=client).render()
            last_n_games = LastNGamesFilter(client=client).render()

    if player:
        row1, row2, row3 = st.container(), st.container(), st.container()

        # Season averages
        with row1:
            SeasonAverage(
                player_id=player,
                season=season,
                client=client,
            ).render()

        # Last N games averages
        with row2:
            RecentGameStats(
                player_id=player,
                opponent_abbrev=(
                    opponent_abbrev if opponent_abbrev is not "All" else None
                ),
                last_n_games=last_n_games,
                client=client,
            ).render()

        with row3:
            RecentGameLogs(
                player_id=player,
                opponent_abbrev=(
                    opponent_abbrev if opponent_abbrev is not "All" else None
                ),
                last_n_games=last_n_games,
                client=client,
            ).render()


if __name__ == "__main__":
    main()
