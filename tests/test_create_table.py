from datetime import date, datetime

from nba_data_forge.etl.extractors.game_log_extractor import GameLogExtractor
from nba_data_forge.etl.transformers.game_log_transformer import GameLogTransformer

extractor = GameLogExtractor()
extractor.extract()
start_date = datetime.strptime("2024-02-01", "%Y-%m-%d")
end_date = datetime.strptime("2024-02-02", "%Y-%m-%d")
df = extractor.extract_date_range(start_date, end_date)
print("Dataset Shape:", df.shape)
print("\nColumn Names:")
print(df.columns.tolist())
print("\nData Types:")
print(df.dtypes)
print(df.head())


# def _load_sql():
#     sql_path = (
#         get_project_root() / "src/nba_data_forge/etl/loaders/sql/test_create_table.sql"
#     )
#     return sql_path.read_text()


# create_table_sql = _load_sql()

# db_url = config.get_sqlalchemy_url()
# engine = create_engine(db_url)

# with engine.connect() as conn:
#     conn.execute(text(create_table_sql))


# df = pd.read_csv(f"./data/temp/game_logs_2006_transformed.csv")
# transformer = GameLogTransformer()
# processed_df = transformer.transform(df)
# print(
#     processed_df[
#         (processed_df["date"] == "2005-11-01")
#         & (processed_df["player_id"] == "abdursh01")
#     ]
# )


# if processed_df.isna().any().any():
#     print("\nRows with NA values:")
#     print(
#         processed_df[processed_df.isna().any(axis=1)][
#             ["team", "opponent", "team_abbrev", "opponent_abbrev"]
#         ]
#     )
#     na_columns = processed_df.columns[processed_df.isna().any()].tolist()
#     print("\nColumns with NA values:")
#     print(na_columns)
