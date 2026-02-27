#!/bin/bash

# Docker Setup Helper Script for AI Virtual Mouse
# This script helps set up Docker and dependencies for running AI Virtual Mouse

set -e

echo "================================"
echo "AI Virtual Mouse Docker Setup"
echo "================================"
echo ""

# Detect OS
OS_TYPE=$(uname -s)
echo "Detected OS: $OS_TYPE"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed."
    echo "📦 Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
else
    echo "✅ Docker is installed: $(docker --version)"
fi

echo ""

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running."
    echo "🚀 Please start Docker Desktop and try again."
    exit 1
else
    echo "✅ Docker daemon is running."
fi

echo ""

# OS-specific setup
case "$OS_TYPE" in
    Linux)
        echo "Setting up Docker for Linux..."
        echo "Allowing local Docker connections to X11..."
        xhost +local:docker 2>/dev/null || echo "⚠️  Could not configure xhost. You may need to run 'xhost +local:docker' manually."
        ;;
    Darwin)
        echo "Setting up Docker for macOS..."
        if ! command -v xquartz-run-xvfb &> /dev/null; then
            echo ""
            echo "ℹ️  For GUI support on macOS, XQuartz is recommended."
            echo "📦 Install XQuartz from: https://www.xquartz.org/"
            echo ""
            echo "To install via Homebrew:"
            echo "  brew install --cask xquartz"
            echo ""
        else
            echo "✅ XQuartz is installed."
        fi
        ;;
    MINGW*|MSYS*)
        echo "Setting up Docker for Windows..."
        echo "ℹ️  For GUI support on Windows, an X server like VcXsrv is recommended."
        echo "📦 Install VcXsrv from: https://sourceforge.net/projects/vcxsrv/"
        ;;
    *)
        echo "⚠️  Unsupported OS: $OS_TYPE"
        ;;
esac

echo ""
echo "================================"
echo "Building Docker Image..."
echo "================================"
echo ""

# Build the Docker image
docker build -t ai-virtual-mouse .

echo ""
echo "================================"
echo "✅ Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Start your X server if you haven't already"
echo "2. Run the container with:"
echo ""
if [ "$OS_TYPE" = "Linux" ]; then
    echo "   xhost +local:docker"
    echo "   docker-compose up"
elif [ "$OS_TYPE" = "Darwin" ]; then
    echo "   export DISPLAY=host.docker.internal:0"
    echo "   xhost +local:docker 2>/dev/null || true"
    echo "   docker-compose up"
else
    echo "   docker-compose up"
fi
echo ""
echo "Or for manual setup:"
echo "   docker run -it --rm --privileged -e DISPLAY=\${DISPLAY} -v /tmp/.X11-unix:/tmp/.X11-unix --device=/dev/video0:/dev/video0 -v \$(pwd)/config.yaml:/app/config.yaml -v \$(pwd)/logs:/app/logs ai-virtual-mouse"
echo ""
