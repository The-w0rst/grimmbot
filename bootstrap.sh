#!/bin/bash
# Quick install script for Grimmbot with progress messages
set -e

REPO_URL="https://github.com/The-w0rst/grimmbot.git"
TARGET_DIR="grimmbot"

TOTAL=5
step=1

echo "Step ${step}/${TOTAL}: Checking prerequisites..."
((step++))
if ! command -v git >/dev/null 2>&1; then
    echo "git is required but not installed." >&2
    exit 1
fi

if command -v python3 >/dev/null 2>&1; then
    PY=python3
elif command -v py >/dev/null 2>&1; then
    PY="py -3"
else
    echo "Python 3.10+ is required." >&2
    exit 1
fi

if ! $PY -m pip --version >/dev/null 2>&1; then
    echo "pip is required but not installed for $PY." >&2
    exit 1
fi

echo "Step ${step}/${TOTAL}: Cloning repository..."
((step++))
if [ ! -d .git ] || [ ! -f install.py ]; then
    if [ ! -d "$TARGET_DIR" ]; then
        git clone "$REPO_URL" "$TARGET_DIR"
    fi
    cd "$TARGET_DIR"
fi

echo "Step ${step}/${TOTAL}: Running installer..."
((step++))
$PY install.py

echo "Step ${step}/${TOTAL}: Running diagnostics..."
if ! $PY diagnostics.py; then
    echo "Diagnostics failed. Check the output above." >&2
fi

((step++))
echo "Step ${step}/${TOTAL}: Launching GoonBot..."
$PY goon_bot.py

echo "Bootstrap complete."

