import logging
from logging.handlers import RotatingFileHandler

from src.server.configs import get_config

from .paths import LOGS_FOLDER

_FORMATTER = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s", "[%d-%b-%y %H:%M:%S]")


def get_file_handler(log_filename: str) -> logging.Handler:
    config = get_config()
    path = LOGS_FOLDER.joinpath(log_filename)
    handler = RotatingFileHandler(
        filename=path,
        maxBytes=config.logging_backup_bytes,
        backupCount=config.logging_backup_count,
    )
    handler.setFormatter(_FORMATTER)
    return handler


def get_stream_handler() -> logging.Handler:
    config = get_config()
    handler = logging.StreamHandler()
    handler.setFormatter(_FORMATTER)
    handler.setLevel(config.logging_level)
    return handler
