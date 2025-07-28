#!/bin/bash
# Quick install script for Grimmbot
set -e

REPO_URL="https://github.com/The-w0rst/grimmbot.git"
TARGET_DIR="grimmbot"

# Clone repository unless we're already inside it
if [ ! -d .git ] || [ ! -f install.py ]; then
    if [ ! -d "$TARGET_DIR" ]; then
        echo "Cloning repository..."
        git clone "$REPO_URL" "$TARGET_DIR"
    fi
    cd "$TARGET_DIR"
fi

# Determine Python executable
if command -v python3 >/dev/null 2>&1; then
    PY=python3
else
    PY=python
fi

# Run interactive installer
$PY install.py

