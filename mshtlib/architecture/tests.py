from os import mkdir
from pathlib import Path


def create_tests():
    mkdir("tests")
    mkdir(Path("tests").joinpath("components"))
    mkdir(Path("tests").joinpath("endpoints"))
