import os
from configparser import ConfigParser
from pathlib import Path

from nba_data_forge.etl.utils.path import get_project_root

ROOT = get_project_root()
print(ROOT)


class Config:
    def __init__(self):
        self.config = ConfigParser()

        # Check multiple possible config locations
        possible_locations = [
            # Docker environment
            Path("/opt/airflow/config/config.ini"),
            # Local development - project root config
            ROOT / "config.ini",
            # Local development - airflow config
            ROOT / "airflow" / "config" / "config.ini",
        ]

        # Try each location until we find one that exists
        for location in possible_locations:
            if location.exists():
                self.config_file = location
                break
        else:
            raise FileNotFoundError(
                "Config file not found in any of these locations:\n"
                + "\n".join(str(p) for p in possible_locations)
            )

        self._load_config()

    def _load_config(self):
        print(f"Loading config from: {self.config_file}")  # Debug info
        self.config.read(self.config_file)
        if not self.config.sections():
            raise ValueError("Config file is empty or invalid.")

    def get_database_url(self):
        try:
            db = self.config["postgresql"]
            return f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"
        except KeyError:
            raise KeyError("Section 'postgresql' not found in the config file.")


config = Config()
