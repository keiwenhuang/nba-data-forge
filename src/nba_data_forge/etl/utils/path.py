from pathlib import Path

from nba_data_forge.etl.config.paths import paths


def get_project_root() -> Path:
    return paths.base_dir
