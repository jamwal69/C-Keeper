# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for GUI, networking tools, and security tools
RUN apt-get update && apt-get install -y \
    # GUI dependencies
    python3-tk \
    xvfb \
    x11-apps \
    # Networking and security tools
    nmap \
    netcat-traditional \
    curl \
    wget \
    git \
    # Build tools for some Python packages
    build-essential \
    # Clean up to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Create necessary directories
RUN mkdir -p logs data/exploits data/payloads data/wordlists data/custom_exploits

# Initialize the database
RUN python scripts/init_db.py

# Set environment variables for GUI
ENV DISPLAY=:99
ENV PYTHONPATH=/app

# Create startup script
RUN echo '#!/bin/bash\n\
# Start virtual display for GUI\n\
Xvfb :99 -screen 0 1920x1080x24 &\n\
\n\
# Wait for display to be ready\n\
sleep 2\n\
\n\
echo "🚀 C-Keeper Docker Container Ready!"\n\
echo "📋 Available commands:"\n\
echo "  python ckeeper.py --gui    # Start GUI interface"\n\
echo "  python ckeeper.py --cli    # Start CLI interface"\n\
echo "  python cli_demo.py         # CLI demonstration"\n\
echo "  python error_check.py      # System health check"\n\
echo "  python docker_test.py      # Docker environment test"\n\
echo ""\n\
\n\
# Execute the command passed to docker run, or start CLI by default\n\
if [ $# -eq 0 ]; then\n\
    python ckeeper.py --cli\n\
else\n\
    exec "$@"\n\
fi' > /app/start.sh

# Make startup script executable
RUN chmod +x /app/start.sh

# Expose common ports that C-Keeper might use
EXPOSE 4444 8080 8443 9999

# Set the startup script as entrypoint
ENTRYPOINT ["/app/start.sh"]

# Default command (can be overridden)
CMD []
