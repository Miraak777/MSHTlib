from shutil import copy
from pathlib import Path
from mshtlib.common_constants import PROJECT_DIR, SystemType
from platform import system
from os import mkdir


def create_scripts():
    mkdir("scripts")
    if system() == SystemType.WINDOWS:
        copy(PROJECT_DIR.joinpath("architecture", "scripts", "cmd", "local_ci.cmd"), Path("scripts"))
    elif system() == SystemType.LINUX:
        copy(PROJECT_DIR.joinpath("architecture", "scripts", "bash", "local_ci.sh"), Path("scripts"))
