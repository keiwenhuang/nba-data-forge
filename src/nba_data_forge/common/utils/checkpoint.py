import datetime
import json
from pathlib import Path
from typing import Dict, List

from nba_data_forge.common.utils.paths import paths


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if hasattr(obj, "value"):  # Handle enum objects like Team
            return obj.value
        return str(obj)  # Fallback for other non-serializable objects


class CheckpointManager:
    def __init__(self):
        self.base_dir = paths.get_path("checkpoints")
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, identifier: str, data: Dict, logger=None):
        checkpoint_path = self.base_dir / f"checkpoint_{identifier}.json"

        try:
            with open(checkpoint_path, "w") as file:
                json.dump(data, file, cls=DateTimeEncoder)
            if logger:
                logger.info(f"Checkpoint saved: {identifier}")
        except Exception as e:
            if logger:
                logger.error(f"Failed to save checkpoint: {str(e)}")
            raise

    def load(self, identifier: str):
        checkpoint_path = self.base_dir / f"checkpoint_{identifier}.json"
        if not checkpoint_path:
            return None

        try:
            with open(checkpoint_path, "r") as file:
                return json.load(file)
        except Exception:
            return None

    def list_all(self) -> List[Path]:
        """List all checkpoint files"""
        return sorted(self.base_dir.glob("checkpoint_*.json"))
