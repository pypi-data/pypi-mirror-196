import os
from pathlib import Path

ROOT_PATH = os.getenv("ROOT_PATH", "/")
DEFAULT_PIPELINES = Path(__file__).parent / "pipelines" / "default.yml"
