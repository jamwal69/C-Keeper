# C-Keeper Quick Installation Guide

This guide helps you get C-Keeper running quickly without manual dependency installation using Docker.

## Prerequisites

- **Docker Desktop** (Windows/macOS) or **Docker Engine** (Linux)
- For GUI mode: X11 server (see platform-specific instructions below)

## Quick Start Options

### Option 1: One-Click Start (Recommended)

**Windows:**
```cmd
# Double-click or run in Command Prompt/PowerShell
quick-start.bat
```

**Linux/macOS:**
```bash
# Make executable and run
chmod +x quick-start.sh
./quick-start.sh
```

### Option 2: Direct Docker Commands

**CLI Mode (No GUI dependencies needed):**
```bash
# Build and run
docker build -t ckeeper .
docker run -it --rm -p 4444:4444 -p 8080:8080 ckeeper python ckeeper.py --cli
```

**GUI Mode:**
```bash
# Build first
docker build -t ckeeper .

# Linux
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -p 4444:4444 ckeeper python ckeeper.py --gui

# Windows (with VcXsrv/Xming running)
docker run -it --rm -e DISPLAY=host.docker.internal:0.0 -p 4444:4444 ckeeper python ckeeper.py --gui

# macOS (with XQuartz running)
docker run -it --rm -e DISPLAY=host.docker.internal:0 -p 4444:4444 ckeeper python ckeeper.py --gui
```

### Option 3: Docker Compose

```bash
# Full environment with persistent data
docker-compose up --build

# Specific profiles
docker-compose --profile gui up
docker-compose --profile redteam up
```

## Platform-Specific GUI Setup

### Windows
1. Install **VcXsrv** or **Xming**
2. Start X server with "Disable access control" enabled
3. Use the GUI option in `quick-start.bat`

### Linux
1. X11 is usually pre-installed
2. Allow Docker access: `xhost +local:docker`
3. Use the GUI option in `quick-start.sh`

### macOS
1. Install **XQuartz**: `brew install --cask xquartz`
2. Start XQuartz and enable "Allow connections from network clients"
3. Use the GUI option in `quick-start.sh`

## Features Available

- ✅ **Complete CLI Interface** - Full penetration testing toolkit
- ✅ **Modern GUI (2025 Edition)** - Beautiful interface with all features
- ✅ **Exploit Builder** - Custom exploit creation
- ✅ **Payload Generator** - Multiple payload types
- ✅ **C2 Handler** - Command and control management
- ✅ **Reconnaissance** - Target discovery and enumeration
- ✅ **Persistent Data** - Your work is saved between sessions

## Persistent Data

When using Docker, your data is automatically persisted:
- **Exploits**: `./data/exploits/`
- **Payloads**: `./data/payloads/`
- **Logs**: `./logs/`
- **Database**: `./data/ckeeper.db`

## Troubleshooting

### Docker Issues
```bash
# Check Docker status
docker --version
docker info

# Health check
docker run --rm ckeeper python error_check.py
```

### GUI Issues
```bash
# Test X11 forwarding
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ckeeper python -c "import tkinter; print('GUI ready!')"
```

### Permission Issues (Linux)
```bash
# Fix X11 permissions
xhost +local:docker
```

## Manual Installation (Alternative)

If Docker isn't available, see the main [README.md](README.md) for manual installation instructions.

## Support

- Check `ERROR_FIXES_SUMMARY.md` for common issues
- Run the health check: `python error_check.py`
- Review logs in `./logs/ckeeper.log`

---

🚀 **Ready to hack? Choose your preferred method above and get started in seconds!**
