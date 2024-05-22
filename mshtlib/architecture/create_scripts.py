from shutil import copytree
from pathlib import Path
from mshtlib.common_constants import PROJECT_DIR


def create_scripts():
    copytree(PROJECT_DIR.joinpath("architecture").joinpath("scripts"), Path("."))

