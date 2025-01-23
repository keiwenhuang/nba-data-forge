import argparse
from pathlib import Path

from data_engineering.extractors.player_extractor import PlayerExtractor


def ensure_data_directories():
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    Path("data/processed").mkdir(parents=True, exist_ok=True)


def collect_player_data():
    player_extractor = PlayerExtractor()
    df = player_extractor.extract()
    df.to_csv("data/raw/players.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--players", action="store_true", help="Collect player data")
    args = parser.parse_args()

    ensure_data_directories()

    if args.players:
        collect_player_data()
