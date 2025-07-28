#!/bin/bash
set -e

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Setup complete. Edit .env with your tokens."
