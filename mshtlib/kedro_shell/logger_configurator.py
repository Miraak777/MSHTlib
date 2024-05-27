from pathlib import Path

from kedro.framework.project import configure_logging


def configurate_kedro_logging(
    log_path: Path, logging_level: str = "INFO", backup_bytes: int = 1000000, backup_count: int = 3
) -> None:
    project_logger_config = {
        "version": 1,
        "root": {"handlers": ["console", "file_handler"], "level": logging_level},
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": logging_level,
                "formatter": "default",
            },
            "file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "default",
                "filename": str(log_path.joinpath("kedro.log")),
                "maxBytes": backup_bytes,
                "backupCount": backup_count,
            },
        },
        "formatters": {
            "default": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s", "datefmt": "%d-%b-%y %H:%M:%S"}
        },
    }
    configure_logging(project_logger_config)
