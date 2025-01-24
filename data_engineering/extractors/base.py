import logging
import time
from abc import ABC, abstractmethod
from logging.handlers import RotatingFileHandler
from pathlib import Path
from random import uniform

import pandas as pd
import requests

from data_engineering.utils.path import get_project_root


class BaseExtractor(ABC):
    def __init__(self, base_url="https://www.basketball-reference.com", log_dir=None):
        self.base_url = base_url
        if log_dir is None:
            root = get_project_root()
            self.log_dir = root / "logs"
        else:
            self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        logger = logging.getLogger(self.__class__.__name__)

        log_file = self.log_dir / f"{self.__class__.__name__}.log"
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(file_handler)

        return logger

    def _handle_rate_limit(self, response, retry_after=60):
        if response.status_code == 429:
            self.logger.warning(
                f"Rate limit exceeded. Waiting {retry_after} seconds..."
            )
            time.sleep(retry_after)
            return requests.get(response.url)
        return response

    def _api_delay(self, delay_range=(3, 7)):
        time.sleep(uniform(*delay_range))

    def _safe_request(self, url, max_retries):
        for attempt in range(max_retries):
            try:
                self.logger.info(f"Getting response...")
                time.sleep(uniform(3, 7))
                response = requests.get(url)
                return self._handle_rate_limit(response)
            except requests.exceptions.RequestException as e:
                self.logger.error(
                    f"Attempt {attempt + 1}/{max_retries} failed for {url}: {str(e)}"
                )
                if attempt == max_retries - 1:
                    raise
                time.sleep(uniform(5, 15))

    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """Extract data and return as DataFrame"""
        pass

    @abstractmethod
    def validate(self, df: pd.DataFrame) -> bool:
        """Validate extracted data"""
        pass
