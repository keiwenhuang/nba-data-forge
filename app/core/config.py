import os
from configparser import ConfigParser


class Config:
    def __init__(self, config_file="config.ini"):
        self.config = ConfigParser()
        self.config_file = config_file
        self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_file):
            print("Config file does not exist.")

        self.config.read(self.config_file)

    def get_database_url(self):
        if "postgresql" in self.config:
            db = self.config["postgresql"]
            db_url = f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"
            return db_url
        else:
            raise KeyError("Section 'postgresql' not found in the config file.")


config = Config()
