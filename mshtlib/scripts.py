from mshtlib.architecture import *
from os import mkdir


def msht_init():
    mkdir("docs")
    mkdir("logs")
    create_src()
    create_tests()
    create_scripts()
    create_settings()
    print("Micro Service initialized successfully.")


def msht_component():
    create_component()
