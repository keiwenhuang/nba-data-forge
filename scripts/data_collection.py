import argparse
import sys

import pandas as pd

from nba_data_forge.common.utils.paths import paths
from nba_data_forge.etl.extractors.game_log_extractor import GameLogExtractor
from nba_data_forge.etl.extractors.player_extractor import PlayerExtractor


def ensure_data_directories():
    root = paths.root
    (root / "data/raw").mkdir(parents=True, exist_ok=True)
    (root / "data/processed").mkdir(parents=True, exist_ok=True)
    (root / "data/checkpoints").mkdir(parents=True, exist_ok=True)


def collect_player_data():
    player_extractor = PlayerExtractor()
    df = player_extractor.extract()
    df.to_csv("data/players/players.csv", index=False)


def collect_game_logs(from_season: int, to_season: int = None):
    root = paths.root
    players = pd.read_csv(root / "data/players/players.csv")
    game_log_extractor = GameLogExtractor(checkpoint_dir=root / "data/checkpoints")

    for season in range(from_season, to_season + 1):
        df = game_log_extractor.extract(players, season=season)
        df.to_csv(root / f"data/raw/game_logs_{season}.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--players", action="store_true", help="Collect player data")
    parser.add_argument("--game-logs", action="store_true", help="Collect game logs")
    parser.add_argument("--from-season", type=int, required="--game-logs" in sys.argv)
    parser.add_argument("--to-season", type=int, default=None)
    args = parser.parse_args()

    ensure_data_directories()

    if args.players:
        collect_player_data()
    if args.game_logs:
        collect_game_logs(args.from_season, args.to_season or args.from_season)
