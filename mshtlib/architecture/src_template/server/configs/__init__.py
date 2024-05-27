from logging import getLogger
from typing import Optional

from src.server.configs.config_model import NlpArgs, NlpConfig

from .tools import create_nlp_config

logger = getLogger(__name__)


def get_config(args: Optional[NlpArgs] = None) -> Optional[NlpConfig]:
    if NlpConfig.get() is None:
        create_nlp_config(args)
    return NlpConfig.get()
