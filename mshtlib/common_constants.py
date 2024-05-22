from pathlib import Path
from dataclasses import dataclass

PROJECT_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class SystemType:
    LINUX: str = "Linux"
    WINDOWS: str = "Windows"
