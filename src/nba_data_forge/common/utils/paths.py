import os
from pathlib import Path
from typing import Dict, Set


class PathManager:
    ARCHIVE_SUBDIRS: Set[str] = {"raw_archive", "transformed_archive"}

    def __init__(self):
        self.is_airflow = bool(os.environ.get("AIRFLOW_HOME"))
        self.project_root = self._detect_root()
        self.paths = self._setup_paths()
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Ensure all directories exist"""
        for path_type, path in self.paths.items():
            try:
                # Create directory if it doesn't exist
                path.mkdir(parents=True, exist_ok=True)

                # Create subdirectories for archive if needed
                if path_type in self.ARCHIVE_SUBDIRS:
                    path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise RuntimeError(
                    f"Failed to create directory for {path_type}: {str(e)}"
                )

    def _detect_root(self) -> Path:
        """Detect project root based on environment"""
        if self.is_airflow:
            airflow_home = os.environ.get("AIRFLOW_HOME")
            if not airflow_home:
                raise ValueError("AIRFLOW_HOME environment variable not set")
            return Path(airflow_home)
        else:
            # local development, go up from this file to project root
            return Path(__file__).parent.parent.parent.parent.parent.resolve()

    def _setup_paths(self) -> Dict[str, Path]:
        """Set up all project paths"""
        data_dir = self.project_root / "data"
        archive_dir = data_dir / "archive"
        test_dir = data_dir / "test"
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
            "checkpoints": data_dir / "checkpoints",
            "sample": data_dir / "sample",
            "test": data_dir / "test",
            "transformed": data_dir / "transformed",
            # archive folders
            "raw_archive": archive_dir / "raw",
            "transformed_archive": archive_dir / "transformed",
            # test folders
            "raw_test": test_dir / "raw",
            "transformed_test": test_dir / "transformed",
        }

    def get_path(self, path_type: str) -> Path:
        """Get specific path by type"""
        if path_type not in self.paths:
            raise ValueError(f"Unknown path type: {path_type}")

        path = self.paths[path_type]
        if not path.exists():
            raise RuntimeError(f"Path does not exist: {path}")
        return path

    def ensure_path_exists(self, path_type: str) -> None:
        """Ensure a specific path exists, creating it if necessary"""
        if path_type not in self.paths:
            raise ValueError(f"Unknown path type: {path_type}")

        self.paths[path_type].mkdir(parents=True, exist_ok=True)

        if path_type in self.ARCHIVE_SUBDIRS:
            self.paths[path_type].mkdir(parents=True, exist_ok=True)

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
