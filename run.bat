@echo off
REM C-Keeper Launcher Script for Windows
REM This script provides easy access to C-Keeper functionality

echo.
echo  ╔═══════════════════════════════════════════════════════════════╗
echo  ║                         C-KEEPER                              ║
echo  ║              Dual-Use Cyber Kill Chain Engine                ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to your PATH
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "ckeeper.py" (
    echo ERROR: ckeeper.py not found
    echo Please run this script from the C-Keeper directory
    pause
    exit /b 1
)

echo Available options:
echo.
echo  1. Initialize Database
echo  2. Run CLI Interface
echo  3. Run GUI Interface  
echo  4. Run Example
echo  5. Install Dependencies
echo  6. Red Team Mode (CLI)
echo  7. Blue Team Mode (CLI)
echo  8. Exit
echo.

set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto init_db
if "%choice%"=="2" goto cli
if "%choice%"=="3" goto gui
if "%choice%"=="4" goto example
if "%choice%"=="5" goto install_deps
if "%choice%"=="6" goto red_team
if "%choice%"=="7" goto blue_team
if "%choice%"=="8" goto exit

echo Invalid choice. Please try again.
pause
goto menu

:init_db
echo.
echo Initializing database...
python scripts\init_db.py
pause
goto menu

:cli
echo.
echo Starting CLI interface...
python ckeeper.py --cli
pause
goto menu

:gui
echo.
echo Starting GUI interface...
python ckeeper.py --gui
pause
goto menu

:example
echo.
echo Running example script...
python example.py
pause
goto menu

:install_deps
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Dependencies installation completed.
pause
goto menu

:red_team
echo.
set /p target="Enter target (IP/CIDR): "
echo Starting red team mode against %target%...
python ckeeper.py --mode red --target %target%
pause
goto menu

:blue_team
echo.
echo Starting blue team monitoring mode...
python ckeeper.py --mode blue --monitor
pause
goto menu

:exit
echo.
echo Goodbye!
exit /b 0

:menu
cls
goto start
