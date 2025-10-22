@echo off
REM Git-SVN Merge - Context Menu Installer for Windows
REM This script installs the right-click context menu integration
REM Run as Administrator

echo ============================================================
echo Git-SVN Merge - Context Menu Installer
echo ============================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo.
    echo Right-click on this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo [OK] Running as Administrator
echo.

REM Get the directory where this batch file is located
set "INSTALL_DIR=%~dp0"
set "INSTALL_DIR=%INSTALL_DIR:~0,-1%"

echo Installation directory: %INSTALL_DIR%
echo.

REM Check if required files exist
echo Checking required files...

if not exist "%INSTALL_DIR%\merge_to_svn.py" (
    echo ERROR: merge_to_svn.py not found in %INSTALL_DIR%
    echo Please ensure all files are in the same directory.
    pause
    exit /b 1
)
echo [OK] merge_to_svn.py found

if not exist "%INSTALL_DIR%\context-menu-handler.ps1" (
    echo ERROR: context-menu-handler.ps1 not found in %INSTALL_DIR%
    echo Please ensure all files are in the same directory.
    pause
    exit /b 1
)
echo [OK] context-menu-handler.ps1 found

echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Python is not installed or not in PATH
    echo The context menu will be installed, but won't work until Python is installed.
    echo Install Python from: https://www.python.org/downloads/
    echo.
    set /p continue="Do you want to continue anyway? (Y/N): "
    if /i not "%continue%"=="Y" (
        echo Installation cancelled.
        pause
        exit /b 0
    )
) else (
    echo [OK] Python is installed
)

echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Git is not installed or not in PATH
    echo The context menu will be installed, but won't work until Git is installed.
    echo Install Git from: https://git-scm.com/
    echo.
    set /p continue="Do you want to continue anyway? (Y/N): "
    if /i not "%continue%"=="Y" (
        echo Installation cancelled.
        pause
        exit /b 0
    )
) else (
    echo [OK] Git is installed
)

echo.
echo ============================================================
echo Creating registry entries...
echo ============================================================
echo.

REM Create temporary registry file with correct paths
set "TEMP_REG=%TEMP%\git-svn-merge-install.reg"

REM Escape backslashes for registry
set "ESCAPED_DIR=%INSTALL_DIR:\=\\%"

REM Create the registry file
(
echo Windows Registry Editor Version 5.00
echo.
echo ; Git-SVN Merge Context Menu Entry
echo.
echo [HKEY_CLASSES_ROOT\Directory\shell\GitSvnMerge]
echo @="Merge Git branch to SVN trunk"
echo "Icon"="C:\\Program Files\\Git\\mingw64\\share\\git\\git-for-windows.ico"
echo.
echo [HKEY_CLASSES_ROOT\Directory\shell\GitSvnMerge\command]
echo @="powershell.exe -ExecutionPolicy Bypass -File \"%ESCAPED_DIR%\\context-menu-handler.ps1\" -RepositoryPath \"%%1\""
echo.
echo [HKEY_CLASSES_ROOT\Directory\Background\shell\GitSvnMerge]
echo @="Merge Git branch to SVN trunk (here)"
echo "Icon"="C:\\Program Files\\Git\\mingw64\\share\\git\\git-for-windows.ico"
echo.
echo [HKEY_CLASSES_ROOT\Directory\Background\shell\GitSvnMerge\command]
echo @="powershell.exe -ExecutionPolicy Bypass -File \"%ESCAPED_DIR%\\context-menu-handler.ps1\" -RepositoryPath \"%%V\""
) > "%TEMP_REG%"

REM Import the registry file
echo Importing registry entries...
reg import "%TEMP_REG%" >nul 2>&1

if errorlevel 1 (
    echo ERROR: Failed to import registry entries
    echo Please check if you have administrator privileges.
    del "%TEMP_REG%" >nul 2>&1
    pause
    exit /b 1
)

echo [OK] Registry entries created successfully
echo.

REM Clean up
del "%TEMP_REG%" >nul 2>&1

echo ============================================================
echo Installation completed successfully!
echo ============================================================
echo.
echo The context menu has been installed.
echo You can now right-click on any folder and select:
echo   "Merge Git branch to SVN trunk"
echo.
echo The script will automatically verify that the folder is a
echo valid git-svn repository before running.
echo.
echo To uninstall, run: uninstall-context-menu.bat
echo.
pause
