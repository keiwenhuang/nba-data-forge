from pathlib import Path

from nba_data_forge.common.config import paths


def get_project_root() -> Path:
    return paths.base_dir
