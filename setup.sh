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

file="config/setup.env"
if [ ! -f "$file" ]; then
    cp config/env_template.env "$file"
fi
echo "Edit $file to add API keys and Discord tokens for all bots."
echo "Setup complete. Run bots with:"
echo "  $PY grimm_bot.py"
echo "  $PY bloom_bot.py"
echo "  $PY curse_bot.py"
echo "  $PY goon_bot.py"

# optionally start a bot immediately when passed as an argument
if [ $# -gt 0 ]; then
    case "$1" in
        grimm)
            exec $PY grimm_bot.py
            ;;
        bloom)
            exec $PY bloom_bot.py
            ;;
        curse)
            exec $PY curse_bot.py
            ;;
        goon)
            exec $PY goon_bot.py
            ;;
        *)
            echo "Unknown bot: $1"
            echo "Valid options are grimm, bloom, curse, or goon."
            ;;
    esac
else
    echo "Run './setup.sh <bot>' to launch one immediately."
fi
