from pathlib import Path

from src.common.const.paths import SRC_PATH

LOG_SETTINGS = Path(__file__).resolve().parent.joinpath("settings.ini")

LOGS_FOLDER = SRC_PATH.parent.joinpath("logs")
LOGS_FOLDER.mkdir(exist_ok=True)
