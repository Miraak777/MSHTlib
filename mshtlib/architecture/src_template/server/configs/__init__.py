from logging import getLogger
from typing import Optional

from src.server.configs.config_model import Args, Config

from .tools import create_nlp_config

logger = getLogger(__name__)


def get_config(args: Optional[Args] = None) -> Optional[Config]:
    if Config.get() is None:
        create_nlp_config(args)
    return Config.get()
