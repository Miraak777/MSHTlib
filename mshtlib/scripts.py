from mshtlib.architecture import create_tests, create_src, create_scripts
from os import mkdir


def ms_init():
    mkdir("docs")
    mkdir("logs")
    create_src()
    create_tests()
    create_scripts()