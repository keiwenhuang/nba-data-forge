import logging
import time
from abc import ABC, abstractmethod
from random import uniform

import pandas as pd
import requests


class BaseExtractor(ABC):
    def __init__(self, base_url="https://www.basketball-reference.com"):
        self.base_url = base_url
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
        )
        return logger

    def _handle_rate_limit(self, response, retry_after=60):
        if response.status_code == 429:
            self.logger.warning(
                f"Rate limit exceeded. Waiting {retry_after} seconds..."
            )
            time.sleep(retry_after)
            return requests.get(response.url)
        return response

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
