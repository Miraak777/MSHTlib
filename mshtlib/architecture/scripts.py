from pathlib import Path
from os import mkdir


def create_scripts():
    mkdir("scripts")
    with Path("scripts").joinpath("local_ci.sh").open("w") as file:
        file.write("""
#!/bin/bash

unittest() {
  echo "--------------------------------------UNITTEST-----------------------------------"
  python3 -m coverage run --source=. -m unittest discover -s ./tests
  echo "---------------------------------------------------------------------------------"
}

coverage() {
  COVERAGE_LIMIT=50 # As in push CI
  echo "--------------------------------------COVERAGE-----------------------------------"
  python3 -m coverage report --fail-under=$COVERAGE_LIMIT -m
  echo "---------------------------------------------------------------------------------"
}

isort() {
  echo "--------------------------------------ISORT--------------------------------------"
  python3 -m isort ./src_template --diff --line-length 120 --check
  echo "---------------------------------------------------------------------------------"

}

black() {
  echo "--------------------------------------BLACK--------------------------------------"
  python3 -m black ./src_template --diff --line-length 120 --color
  echo "---------------------------------------------------------------------------------"
}

pylint() {
  echo "--------------------------------------PYLINT-------------------------------------"
  python3 -m pylint ./src_template
  echo "---------------------------------------------------------------------------------"
}
activate () {
  source venv/bin/activate
}

help() {
  echo "usage: ./scripts/local_ci.sh [-h] [-t] [-c] [-i] [-b] [-p] [-a]"
  echo
  echo "Check changed code before pushing"
  echo
  echo "arguments:"
  echo "  -h     show this help message and exit"
  echo "  -t     run unittest"
  echo "  -c     run coverage utility"
  echo "  -i     run isort"
  echo "  -b     run black"
  echo "  -p     run pylint"
  echo "  -a     run all checks"
  echo
}

if [ $# -lt 1 ]; then
  echo "No options found!"
  exit 1
fi


activate
while getopts "tcibpah" option; do
  case $option in
  t)
    unittest
    ;;
  c)
    coverage
    ;;
  i)
    isort
    ;;
  b)
    black
    ;;
  p)
    pylint
    ;;
  a)
    unittest
    coverage
    isort
    black
    pylint
    ;;
  h)
    help
    exit
    ;;
  \?) # incorrect option
    echo "Error: Invalid option"
    exit
    ;;
  esac
done

            """)