from dataclasses import dataclass


@dataclass(frozen=True)
class LoggerConfigConst:
    LOGGING_SECTION: str = "LOGGING"
    LEVEL: str = "level"
    BACKUP_BYTES: str = "backup_bytes"
    BACKUP_COUNT: str = "backup_count"
