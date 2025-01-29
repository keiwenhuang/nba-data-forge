import os
from configparser import ConfigParser
from data_engineering.utils.path import get_project_root

ROOT = get_project_root()


class Config:
    def __init__(self, config_file=f"{ROOT}/config.ini"):
        self.config = ConfigParser()
        self.config_file = config_file
        self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file {self.config_file} does not exist.")

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
