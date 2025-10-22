@echo off
REM Git-SVN Merge Automation Script - Windows Wrapper
REM This wrapper makes it easier to run the Python script on Windows

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    exit /b 1
)

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0

REM Run the Python script with all arguments passed to this batch file
python "%SCRIPT_DIR%merge_to_svn.py" %*
