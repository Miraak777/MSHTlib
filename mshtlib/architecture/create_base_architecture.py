from os import mkdir
from mshtlib.architecture import create_tests, create_src, create_scripts

mkdir("docs")
mkdir("logs")
create_src()
create_tests()
create_scripts()
