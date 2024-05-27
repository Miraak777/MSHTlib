import logging

from mshtlib.kedro_shell.logger_configurator import configurate_kedro_logging

from src.server.configs import get_config

from .handlers import get_file_handler, get_stream_handler
from .paths import LOGS_FOLDER


def set_project_logging(top_name: str) -> None:
    stream_handler = get_stream_handler()
    project_file_handler = get_file_handler("project.log")

    top_logger = logging.getLogger(top_name)
    top_logger.addHandler(stream_handler)
    top_logger.addHandler(project_file_handler)

    config = get_config()

    configurate_kedro_logging(
        log_path=LOGS_FOLDER,
        logging_level=logging.getLevelName(config.logging_level),
        backup_bytes=config.logging_backup_bytes,
        backup_count=config.logging_backup_count,
    )


def set_server_logger() -> None:
    stream_handler = get_stream_handler()

    logger = logging.getLogger("werkzeug")
    logger.handlers = [stream_handler]
    logger.propagate = False
