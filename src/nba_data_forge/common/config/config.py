from configparser import ConfigParser

from nba_data_forge.common.utils.paths import paths


class Config:
    def __init__(self):
        self.config = ConfigParser()
        self.is_airflow = paths.is_airflow
        self._load_config()

    # def _detect_environment(self) -> Literal["airflow", "local"]:
    #     """Detect if running in Airflow or local"""
    #     return "airflow" if Path("/.dockerenv").exists() else "local"

    # def _get_config_location(self) -> Path:
    #     """Get config file location based on environment"""
    #     if self.environment == "airflow":
    #         path = Path("/opt/airflow/config/config.ini")
    #     else:
    #         path = ROOT / "config.ini"

    #     if not path.exists():
    #         raise FileNotFoundError(f"Config file not found at {path}")

    #     self.logger.info(f"Using config file: {path}")
    #     return path

    def _load_config(self):
        """Load configuration from appropriate location"""
        config_file = paths.config_file
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found at {config_file}")

        self.config.read(config_file)
        if not self.config.sections():
            raise ValueError("Config file is empty or invalid")

    def get_database_url(self, test=False):
        """Get database URL with environment-appropriate host"""
        try:
            section = "postgresql_test" if test else "postgresql"
            db = self.config[section]

            # Use host.docker.internal in Airflow, otherwise use config host
            host = "host.docker.internal" if self.is_airflow else db["host"]

            return f"postgresql://{db['user']}:{db['password']}@{host}:{db['port']}/{db['database']}"
        except KeyError:
            raise KeyError(f"Section '{section}' not found in config")

    def get_sqlalchemy_url(self):
        """Get SQLAlchemy-specific URL with psycopg2 driver"""
        return self.get_database_url().replace(
            "postgresql://", "postgresql+psycopg2://"
        )


config = Config()
