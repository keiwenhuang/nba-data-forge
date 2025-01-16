from datetime import datetime

import numpy as np
import pandas as pd


def explore_data():
    """Explore NBA game logs data by printing data types and unique values.

    Reads CSV file and displays:
    1. Data types of all columns
    2. Unique values for team, location, opponent, and outcome fields
    """
    game_logs = pd.read_csv("./data/players_all_game_logs.csv")

    print("Data Type:")
    print(game_logs.dtypes)
    print("-" * 75)

    uniqueness = ["team", "location", "opponent", "outcome"]
    for item in uniqueness:
        print(f"\nUnique {item.title()}:")
        unique_values = game_logs[item].unique()
        print(sorted(unique_values[~pd.isna(unique_values)]))
        print("-" * 75)

    # Print longest value in each column
    print("\nLongest values in each column:")
    for column in game_logs.columns:
        max_len_value = max(game_logs[column].astype(str), key=len)
        print(f"{column}: {max_len_value} (length: {len(str(max_len_value))})")
    print("-" * 75)


def clean_field(item) -> str | None:
    """Clean field by removing prefix and replacing underscores with spaces for team names.

    Args:
        item: Raw string value
    Returns:
        Cleaned string or None if input is NA
    """
    if pd.isna(item):
        return None

    item = item.split(".")[1]
    if "_" in item:
        item = item.replace("_", " ")

    return item


def preprocess_data():
    df = pd.read_csv("./data/players_all_game_logs.csv")

    # convert data type
    df["date"] = pd.to_datetime(df["date"])
    df["is_home"] = df["location"].eq("Location.HOME")
    df["is_win"] = df["outcome"].eq("Outcome.WIN")
    df["minutes_played"] = round(df["seconds_played"] / 60, 3)

    columns = ["team", "location", "opponent", "outcome"]
    for col in columns:
        df[col] = df[col].apply(clean_field)

    # save the processed data
    df.to_csv("./data/processed_game_logs.csv", index=False)

    print(df.head())
    print(df.dtypes)


if __name__ == "__main__":
    explore_data()
    preprocess_data()
