from argparse import ArgumentParser
from pathlib import Path
from typing import Optional

from src.common.logger import set_project_logging, set_server_logger
from src.server.configs import Args, get_config
from src.server.routes import app


def main() -> None:
    args = parsing()
    config = get_config(args)
    set_project_logging(__name__)
    set_server_logger()
    app.run(host=config.server_host, port=config.server_port, debug=False)


def parsing() -> Optional[Args]:
    parser = ArgumentParser(description="Run NLP Service")
    parser.add_argument("-b", "--host", "--bind", help="server host", type=str)
    parser.add_argument("-p", "--port", help="server port", type=str)
    parser.add_argument("-c", "--config", help="config.ini file path", type=Path)
    args = parser.parse_args(namespace=Args())
    return args


if __name__ == "__main__":
    main()
