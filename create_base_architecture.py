from os import mkdir
from mshtlib.architecture import create_tests, create_src, create_scripts


def create_architecture():
    mkdir("docs")
    mkdir("logs")
    create_src()
    create_tests()
    create_scripts()
