#!/bin/bash
# Simple setup script for Goon Squad bots
set -e

echo "== Goon Squad Setup =="

# install Python dependencies
if command -v python3 >/dev/null 2>&1; then
    PY=python3
else
    PY=python
fi

$PY -m pip install --user -r requirements.txt

# create config directory if missing
mkdir -p config

for bot in grimm bloom curse; do
    file="config/${bot}.env"
    echo "Edit $file to add API keys and Discord token."
done
echo "Setup complete. Run bots with:"
echo "  $PY grimm_bot.py"
echo "  $PY bloom_bot.py"
echo "  $PY curse_bot.py"
