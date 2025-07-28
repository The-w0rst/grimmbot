# Grimmbot Multi-Bot Setup

This project contains three simple Discord bots using OpenAI API. Each bot runs from its own file inside the `bots/` directory.

## Setup

1. Copy `config.env.example` to `.env` and fill in your Discord tokens and API keys.
2. Run `./setup.sh` to create a Python virtual environment and install dependencies.
3. Start all bots with `./run.sh`.

## Files

- `bots/bot1.py`, `bots/bot2.py`, `bots/bot3.py` – individual bot scripts
- `setup.sh` – create virtual environment and install requirements
- `run.sh` – launch all bots using the credentials from `.env`

Each bot responds to messages starting with `!bot1`, `!bot2`, or `!bot3` respectively, using the text after that command as a prompt for OpenAI.
