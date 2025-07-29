#!/bin/bash
# Pull the latest Grimmbot code and rerun the installer
set -e

if [ ! -f install.py ]; then
    echo "Run this script from the repository root." >&2
    exit 1
fi

git pull

if command -v python3 >/dev/null 2>&1; then
    PY=python3
elif command -v py >/dev/null 2>&1; then
    PY="py -3"
else
    PY=python
fi

$PY install.py

echo "Update complete."

