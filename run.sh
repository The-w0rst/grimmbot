#!/bin/bash
set -e
source venv/bin/activate

# load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

python bots/bot1.py &
python bots/bot2.py &
python bots/bot3.py &

wait
