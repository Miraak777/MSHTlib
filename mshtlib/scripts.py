from mshtlib.architecture import create_tests, create_src, create_scripts, create_settings
from os import mkdir


def ms_init():
    mkdir("docs")
    mkdir("logs")
    create_src()
    create_tests()
    create_scripts()
    create_settings()
    print("Micro Service initialized successfully.")
