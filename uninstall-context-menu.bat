@echo off
REM Git-SVN Merge - Context Menu Uninstaller for Windows
REM This script removes the right-click context menu integration
REM Run as Administrator

echo ============================================================
echo Git-SVN Merge - Context Menu Uninstaller
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

echo This will remove the "Merge Git branch to SVN trunk" option
echo from the Windows Explorer context menu.
echo.
set /p confirm="Are you sure you want to continue? (Y/N): "

if /i not "%confirm%"=="Y" (
    echo.
    echo Uninstallation cancelled.
    pause
    exit /b 0
)

echo.
echo Removing registry entries...
echo.

REM Remove the registry keys
reg delete "HKEY_CLASSES_ROOT\Directory\shell\GitSvnMerge" /f >nul 2>&1
if errorlevel 1 (
    echo Warning: Could not remove Directory\shell\GitSvnMerge
) else (
    echo [OK] Removed Directory context menu entry
)

reg delete "HKEY_CLASSES_ROOT\Directory\Background\shell\GitSvnMerge" /f >nul 2>&1
if errorlevel 1 (
    echo Warning: Could not remove Directory\Background\shell\GitSvnMerge
) else (
    echo [OK] Removed Directory Background context menu entry
)

echo.
echo ============================================================
echo Uninstallation completed!
echo ============================================================
echo.
echo The context menu entries have been removed.
echo.
echo Note: The script files are still in this directory.
echo You can manually delete them if you no longer need them.
echo.
pause
