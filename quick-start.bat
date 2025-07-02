@echo off
echo ===============================================
echo           C-Keeper Quick Start (Windows)
echo ===============================================
echo.

:: Check if Docker is installed
docker --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Docker is not installed or not in PATH
    echo.
    echo Please install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop/
    echo.
    pause
    exit /b 1
)

echo ✅ Docker found!
echo.

:: Check if Docker is running
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Docker is not running
    echo.
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)

echo ✅ Docker is running!
echo.

:: Offer installation options
echo Choose your preferred method:
echo.
echo 1. CLI Mode (Recommended for beginners)
echo 2. GUI Mode (Requires X11 server on Windows)
echo 3. Build and run with Docker Compose
echo 4. Interactive Docker shell
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto cli_mode
if "%choice%"=="2" goto gui_mode
if "%choice%"=="3" goto compose_mode
if "%choice%"=="4" goto shell_mode

echo Invalid choice. Starting CLI mode...

:cli_mode
echo.
echo 🚀 Starting C-Keeper in CLI mode...
echo.
docker build -t ckeeper .
docker run -it --rm --name ckeeper-cli -p 4444:4444 -p 8080:8080 -v "%cd%\data:/app/data" -v "%cd%\logs:/app/logs" ckeeper python ckeeper.py --cli
goto end

:gui_mode
echo.
echo 📋 GUI Mode Requirements for Windows:
echo   - Install VcXsrv or Xming (X11 server)
echo   - Start X11 server with "Disable access control" enabled
echo   - Set DISPLAY environment variable
echo.
echo Starting C-Keeper in GUI mode...
echo.
docker build -t ckeeper .
docker run -it --rm --name ckeeper-gui -e DISPLAY=host.docker.internal:0.0 -p 4444:4444 -p 8080:8080 -v "%cd%\data:/app/data" -v "%cd%\logs:/app/logs" ckeeper python ckeeper.py --gui
goto end

:compose_mode
echo.
echo 🐳 Starting with Docker Compose...
echo.
docker-compose up --build
goto end

:shell_mode
echo.
echo 🔧 Starting interactive Docker shell...
echo.
docker build -t ckeeper .
docker run -it --rm --name ckeeper-shell -p 4444:4444 -p 8080:8080 -v "%cd%\data:/app/data" -v "%cd%\logs:/app/logs" ckeeper /bin/bash
goto end

:end
echo.
echo Thanks for using C-Keeper!
pause
