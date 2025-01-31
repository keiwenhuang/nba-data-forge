from datetime import date

from nba_data_forge.api.dependencies.filters import CommonQueryParams
from nba_data_forge.api.models.game_log import GameLog as GameLogModel


def get_season_date_range(season: int):
    season_start = date(season - 1, 10, 1)
    season_end = date(season, 6, 30)
    return season_start, season_end


def apply_common_filters(query, commons: CommonQueryParams):
    if commons.season:
        season_start, season_end = get_season_date_range(commons.season)
        query = query.filter(
            GameLogModel.date >= season_start, GameLogModel.date <= season_end
        )
    elif commons.start_date or commons.end_date:
        # If no season specified, use explicit date filters if provided
        if commons.start_date:
            query = query.filter(GameLogModel.date >= commons.start_date)
        if commons.end_date:
            query = query.filter(GameLogModel.date <= commons.end_date)

    query = query.order_by(GameLogModel.date.desc())

    if commons.last_n_games:
        query = query.limit(commons.last_n_games)

    return query


def check_record_exists(db, model, **filters) -> bool:
    """Check if a record exists in the database."""
    return db.query(db.query(model).filter_by(**filters).exists()).scalar()
