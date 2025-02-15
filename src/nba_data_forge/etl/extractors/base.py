import time
from abc import ABC, abstractmethod
from random import uniform
from typing import Dict, Optional

import pandas as pd
import requests

from nba_data_forge.common.utils.checkpoint import CheckpointManager
from nba_data_forge.common.utils.logger import setup_logger
from nba_data_forge.common.utils.paths import paths


class BaseExtractor(ABC):
    def __init__(self, base_url="https://www.basketball-reference.com", test=False):
        self.base_url = base_url
        self.checkpoint_manager = CheckpointManager()
        self.logger = setup_logger(
            name=self.__class__.__name__, log_dir=paths.get_path("logs")
        )
        self.test = test

    def save_checkpoint(self, identifier: str, data: Dict[str, any]) -> None:
        self.checkpoint_manager.save(identifier, data, self.logger)

    def load_checkpoint(self, identifier: str) -> Optional[Dict[str, any]]:
        return self.checkpoint_manager.load(identifier)

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
