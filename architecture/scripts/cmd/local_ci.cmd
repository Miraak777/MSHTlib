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
