#!/bin/bash

# C-Keeper Quick Start Script for Linux/macOS
# This script automates the Docker setup and provides easy deployment options

set -e  # Exit on any error

echo "==============================================="
echo "           C-Keeper Quick Start (Linux/macOS)"
echo "==============================================="
echo

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo
    echo "Please install Docker from:"
    echo "https://docs.docker.com/get-docker/"
    echo
    exit 1
fi

echo -e "${GREEN}✅ Docker found!${NC}"

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker is not running${NC}"
    echo
    echo "Please start Docker and try again."
    echo
    exit 1
fi

echo -e "${GREEN}✅ Docker is running!${NC}"
echo

# Check if Docker Compose is available
COMPOSE_CMD=""
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
fi

# Show menu
echo "Choose your preferred method:"
echo
echo "1. CLI Mode (Recommended for beginners)"
echo "2. GUI Mode (Requires X11 forwarding)"
echo "3. Build and run with Docker Compose"
echo "4. Interactive Docker shell"
echo "5. Health check"
echo

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo
        echo -e "${BLUE}🚀 Starting C-Keeper in CLI mode...${NC}"
        echo
        docker build -t ckeeper .
        docker run -it --rm --name ckeeper-cli \
            -p 4444:4444 -p 8080:8080 \
            -v "$(pwd)/data:/app/data" \
            -v "$(pwd)/logs:/app/logs" \
            ckeeper python ckeeper.py --cli
        ;;
    2)
        echo
        echo -e "${YELLOW}📋 GUI Mode Requirements:${NC}"
        echo "   - X11 forwarding enabled"
        echo "   - DISPLAY environment variable set"
        echo
        echo -e "${BLUE}Starting C-Keeper in GUI mode...${NC}"
        echo
        
        # Set up X11 forwarding for Linux
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            xhost +local:docker 2>/dev/null || echo "Warning: Could not enable X11 forwarding"
            DISPLAY_VAR="${DISPLAY:-:0}"
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS with XQuartz
            DISPLAY_VAR="host.docker.internal:0"
        else
            DISPLAY_VAR=":0"
        fi
        
        docker build -t ckeeper .
        docker run -it --rm --name ckeeper-gui \
            -e DISPLAY="$DISPLAY_VAR" \
            -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
            -p 4444:4444 -p 8080:8080 \
            -v "$(pwd)/data:/app/data" \
            -v "$(pwd)/logs:/app/logs" \
            ckeeper python ckeeper.py --gui
        ;;
    3)
        echo
        echo -e "${BLUE}🐳 Starting with Docker Compose...${NC}"
        echo
        if [[ -z "$COMPOSE_CMD" ]]; then
            echo -e "${RED}❌ Docker Compose not found${NC}"
            echo "Please install Docker Compose"
            exit 1
        fi
        $COMPOSE_CMD up --build
        ;;
    4)
        echo
        echo -e "${BLUE}🔧 Starting interactive Docker shell...${NC}"
        echo
        docker build -t ckeeper .
        docker run -it --rm --name ckeeper-shell \
            -p 4444:4444 -p 8080:8080 \
            -v "$(pwd)/data:/app/data" \
            -v "$(pwd)/logs:/app/logs" \
            ckeeper /bin/bash
        ;;
    5)
        echo
        echo -e "${BLUE}🏥 Running health check...${NC}"
        echo
        docker build -t ckeeper .
        docker run --rm --name ckeeper-health \
            -v "$(pwd)/data:/app/data" \
            -v "$(pwd)/logs:/app/logs" \
            ckeeper python error_check.py
        ;;
    *)
        echo "Invalid choice. Starting CLI mode..."
        docker build -t ckeeper .
        docker run -it --rm --name ckeeper-cli \
            -p 4444:4444 -p 8080:8080 \
            -v "$(pwd)/data:/app/data" \
            -v "$(pwd)/logs:/app/logs" \
            ckeeper python ckeeper.py --cli
        ;;
esac

echo
echo -e "${GREEN}Thanks for using C-Keeper!${NC}"
