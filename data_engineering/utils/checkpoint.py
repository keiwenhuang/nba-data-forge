import datetime
import json
from pathlib import Path
from typing import Dict, List


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if hasattr(obj, "value"):  # Handle enum objects like Team
            return obj.value
        return str(obj)  # Fallback for other non-serializable objects


class CheckpointManager:
    def __init__(self, base_dir="data/checkpoints"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_checkpoint(self, season: int, idx: int, data: List[Dict], logger=None):
        checkpoint = {"season": season, "idx": idx, "data": data}
        checkpoint_path = self.base_dir / f"checkpoint_{season}.json"

        try:
            with open(checkpoint_path, "w") as file:
                json.dump(checkpoint, file, cls=DateTimeEncoder)
            if logger:
                logger.info(f"Checkpoint saved: season {season}, player {idx}")
        except Exception as e:
            if logger:
                logger.error(f"Failed to save checkpoint: {str(e)}")
            raise

    def load_latest_checkpoint(self, season: int):
        checkpoints = list(self.base_dir.glob(f"checkpoint_{season}.json"))
        if not checkpoints:
            return None

        latest = max(checkpoints, key=lambda x: x.stem.split("_")[-1])

        try:
            with open(latest, "r") as file:
                return json.load(file)
        except Exception:
            return None

    def list_checkpoints(self, season: int = None) -> List[Path]:
        """List all checkpoints, optionally filtered by season"""
        pattern = f"checkpoint_{season}.json" if season else "checkpoint_*.json"
        return sorted(self.base_dir.glob(pattern))
