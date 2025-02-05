import os
from pathlib import Path
from typing import Dict


class PathManager:
    def __init__(self):
        self.is_airflow = bool(os.environ.get("AIRFLOW_HOME"))
        self.project_root = self._detect_root()
        self.paths = self._setup_paths()

    def _detect_root(self) -> Path:
        """Detect project root based on environment"""
        if self.is_airflow:
            return Path("/opt/airflow")
        else:
            # local development, go up from this file to project root
            return Path(__file__).parent.parent.parent.parent.parent.resolve()

    def _setup_paths(self) -> Dict[str, Path]:
        """Set up all project paths"""
        data_dir = self.project_root / "data"
        return {
            "root": self.project_root,
            "config": self.project_root / "config",
            "logs": self.project_root / "logs",
            # data folders
            "data": data_dir,
            "raw": data_dir / "raw",
            "processed": data_dir / "processed",
            "temp": data_dir / "temp",
            "archive": data_dir / "archive",
            "raw_archive": data_dir / "archive/raw",
            "transformed_archive": data_dir / "archive/transformed",
            "checkpoints": data_dir / "checkpoints",
        }

    def get_path(self, path_type: str) -> Path:
        """Get specific path by type"""
        if path_type not in self.paths:
            raise ValueError(f"Unknown path type: {path_type}")
        return self.paths[path_type]

    @property
    def root(self) -> Path:
        """Get project root path"""
        return self.project_root

    @property
    def config_file(self) -> Path:
        """Get appropriate config file path"""
        if self.is_airflow:
            return Path("/opt/airflow/config/config.ini")
        return self.project_root / "config.ini"


paths = PathManager()
