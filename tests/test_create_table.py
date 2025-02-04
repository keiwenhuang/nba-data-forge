from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from nba_data_forge.common.config.config import config
from nba_data_forge.common.utils.path import get_project_root
from nba_data_forge.etl.transformers.game_log_transformer import GameLogTransformer


def _load_sql():
    sql_path = (
        get_project_root() / "src/nba_data_forge/etl/loaders/sql/test_create_tables.sql"
    )
    return sql_path.read_text()


create_table_sql = _load_sql()

db_url = config.get_sqlalchemy_url()
engine = create_engine(db_url)

with engine.connect() as conn:
    conn.execute(text(create_table_sql))

df = pd.read_csv("./data/raw/game_logs_2009.csv")
sample = df.sample(n=30)
# print(sample.head())


transformer = GameLogTransformer()
processed_df = transformer.transform(sample)
# print("\nRows with NA values:")
# print(
#     processed_df[processed_df.isna().any(axis=1)][
#         ["team", "opponent", "team_abbrev", "opponent_abbrev"]
#     ]
# )

# na_columns = processed_df.columns[processed_df.isna().any()].tolist()
# print("\nColumns with NA values:")
# print(na_columns)

processed_df.to_sql("test_game_logs", engine, if_exists="append", index=False)
