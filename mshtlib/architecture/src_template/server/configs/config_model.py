from dataclasses import Field, dataclass, fields
from logging import getLevelName, getLogger
from pathlib import Path
from typing import Callable, Union

logger = getLogger(__name__)


@dataclass
class Args:
    host: str = None
    port: int = None
    auth_public_key: str = None
    config: Path = None


class BaseConfigModel:
    def apply_field(self, field: Field, preprocessing: Callable = None) -> None:
        preprocessing = preprocessing if preprocessing else field.type
        try:
            self.__dict__[field.name] = preprocessing(self.__dict__[field.name])
        except ValueError:
            pass


@dataclass
class Config(BaseConfigModel):
    _instance = None

    server_host: str
    server_port: int
    logging_level: Union[str, int]
    logging_backup_bytes: int
    logging_backup_count: int

    @classmethod
    def get(cls):
        return cls._instance

    def __post_init__(self) -> None:
        postprocessing_map = {
            "logging_level": getLevelName,
        }
        for field in fields(self):
            if field.name in postprocessing_map:
                self.apply_field(field, postprocessing_map[field.name])
            else:
                self.apply_field(field)
        Config._instance = self

