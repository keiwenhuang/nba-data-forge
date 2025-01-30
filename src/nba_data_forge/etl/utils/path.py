import os
from pathlib import Path


def get_project_root() -> Path:
    """Get project paths based on environment"""
    # Check if running in Docker
    if os.environ.get("AIRFLOW_HOME"):
        # Docker paths
        return Path()
    else:
        # Local development paths
        return Path(__file__).parent.parent.parent.parent.parent.resolve()
