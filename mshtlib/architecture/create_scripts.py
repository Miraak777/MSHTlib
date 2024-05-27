from pathlib import Path
from mshtlib.common_constants import SystemType
from platform import system
from os import mkdir
from typing import TextIO


def create_scripts():
    mkdir("scripts")
    if system() == SystemType.WINDOWS:
        with open(Path("scripts").joinpath("local_ci.cmd")) as script_file:
            write_local_ci_cmd(script_file)
    elif system() == SystemType.LINUX:
        with open(Path("scripts").joinpath("local_ci.sh")) as script_file:
            write_local_ci_sh(script_file)


def write_local_ci_cmd(file: TextIO):
    file.write("""
            @echo off

:unittest
echo --------------------------------------UNITTEST-----------------------------------
python -m coverage run --source=. -m unittest discover -s ./tests
echo ---------------------------------------------------------------------------------
goto :eof

:coverage
set COVERAGE_LIMIT=50
echo --------------------------------------COVERAGE-----------------------------------
python -m coverage report --fail-under=%COVERAGE_LIMIT% -m
echo ---------------------------------------------------------------------------------
goto :eof

:isort
echo --------------------------------------ISORT--------------------------------------
python -m isort ./src --diff --line-length 120 --check
echo ---------------------------------------------------------------------------------
goto :eof

:black
echo --------------------------------------BLACK--------------------------------------
python -m black ./src --diff --line-length 120 --color
echo ---------------------------------------------------------------------------------
goto :eof

:pylint
echo --------------------------------------PYLINT-------------------------------------
python -m pylint ./src
echo ---------------------------------------------------------------------------------
goto :eof

:activate
call venv\Scripts\activate
goto :eof

:help
echo usage: local_ci.cmd [-h] [-t] [-c] [-i] [-b] [-p] [-a]
echo.
echo Check changed code before pushing
echo.
echo arguments:
echo   -h     show this help message and exit
echo   -t     run unittest
echo   -c     run coverage utility
echo   -i     run isort
echo   -b     run black
echo   -p     run pylint
echo   -a     run all checks
echo.
goto :eof

if "%~1"=="" (
    echo No options found!
    exit /b 1
)

call :activate

:processargs
if "%~1"=="" goto :eof
if "%~1"=="-t" call :unittest
if "%~1"=="-c" call :coverage
if "%~1"=="-i" call :isort
if "%~1"=="-b" call :black
if "%~1"=="-p" call :pylint
if "%~1"=="-a" (
    call :unittest
    call :coverage
    call :isort
    call :black
    call :pylint
)
if "%~1"=="-h" call :help & exit /b
shift
goto :processargs

            """)

def write_local_ci_sh(file: TextIO):
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
  python3 -m isort ./src --diff --line-length 120 --check
  echo "---------------------------------------------------------------------------------"

}

black() {
  echo "--------------------------------------BLACK--------------------------------------"
  python3 -m black ./src --diff --line-length 120 --color
  echo "---------------------------------------------------------------------------------"
}

pylint() {
  echo "--------------------------------------PYLINT-------------------------------------"
  python3 -m pylint ./src
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