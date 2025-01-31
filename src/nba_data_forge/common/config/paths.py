import os
from pathlib import Path
from typing import Dict


class PathConfig:
    def __init__(self):
        self.is_airflow = bool(os.environ.get("AIRFLOW_HOME"))
        self.base_dir = self._get_base_dir()
        self.paths = self._setup_paths()

    def _get_base_dir(self) -> Path:
        if self.is_airflow:
            return Path("/opt/airflow")
        else:
            # local development, go up from this file to project root
            return Path(__file__).parent.parent.parent.parent.parent.resolve()

    def _setup_paths(self) -> Dict[str, Path]:
        data_dir = self.base_dir / "data"
        return {
            "data": data_dir,
            "raw": data_dir / "raw",
            "processed": data_dir / "processed",
            "temp": data_dir / "temp",
            "logs": data_dir / "logs",
            "sample": data_dir / "sample",
        }

    def get_path(self, path_type: str) -> Path:
        """Get specific path by type"""
        if path_type not in self.paths:
            raise ValueError(f"Unknown path type: {path_type}")
        return self.paths[path_type]


paths = PathConfig()
