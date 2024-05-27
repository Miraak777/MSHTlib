from pathlib import Path
from typing import Any, Dict, List, Optional

import config as conf
import dacite

from src.common.const.paths import PROJECT_ROOT
from src.server.configs.config_model import Args, Config

DEFAULT_CONFIG_PATH = PROJECT_ROOT.joinpath("settings.ini")


def get_path(default_path: Path, dotenv_file_path: Path = None) -> Optional[Path]:
    if dotenv_file_path:
        return dotenv_file_path
    if default_path.exists():
        return default_path
    return None


def form_config_parsing_pipeline(config_file_path: Path = None) -> List[conf.Configuration]:
    pipeline = [conf.config_from_env(prefix="NLP", separator="_", lowercase_keys=False)]
    if config_file_path.exists():
        pipeline.append(conf.config_from_ini(data=str(DEFAULT_CONFIG_PATH), read_from_file=True, lowercase_keys=False))
    else:
        raise FileExistsError(f"Config file {str(config_file_path)} not exist")
    return pipeline


def config_postprocessing(config_parser: conf.ConfigurationSet) -> Dict[str, str]:
    config = config_parser.as_dict()
    return {key.lower().replace(".", "_"): value for key, value in config.items()}


def get_args_map(args: Optional[Args]) -> Optional[Dict[str, Any]]:
    return (
        {}
        if not args
        else {
            "server_host": args.host,
            "server_port": args.port,
        }
    )


def apply_cli_args(config: Dict[str, str], args_map: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in args_map.items():
        if value:
            config[key] = value
    return config


def create_nlp_config(args: Optional[Args]) -> None:
    config_path = args.config if args and args.config else DEFAULT_CONFIG_PATH
    parser = conf.ConfigurationSet(*form_config_parsing_pipeline(config_path))
    config = config_postprocessing(parser)
    config = apply_cli_args(config, get_args_map(args))
    dacite_conf = dacite.Config()
    dacite_conf.check_types = False
    dacite.from_dict(data_class=Config, data=config, config=dacite_conf)
