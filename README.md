# Reaper Gaming Profile Discord Bots

This repository contains three simple Discord bots that can be run from your desktop.
Each bot has a unique personality and command prefix.

## Bots Included

- **GrimBot** (`!` prefix) - Greets users in a spooky style.
- **CurseBot** (`?` prefix) - Playfully curses the user on command.
- **BloomBot** (`&` prefix) - Spreads good vibes to everyone.

## Requirements

- Python 3.11+
- `discord.py` (see `requirements.txt`)

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Running a Bot

Use `run.py` to start any of the bots. Provide the name of the bot and a Discord token
(either via `--token` or the `DISCORD_TOKEN` environment variable).

```bash
python run.py grimbot --token YOUR_TOKEN_HERE
```

Replace `grimbot` with `cursebot` or `bloombot` to run the other bots.

## Running Multiple Bots Together

You can launch more than one bot at the same time using `run_all.py`. Provide the
tokens via command line flags or environment variables (`GRIMBOT_TOKEN`,
`CURSEBOT_TOKEN`, `BLOOMBOT_TOKEN`). Any bots without tokens will not be started.

```bash
python run_all.py --grimbot-token TOKEN1 --cursebot-token TOKEN2
```

The example above starts GrimBot and CurseBot concurrently.

## About Reaper Gaming Profile

All of these bots are configured for the Reaper Gaming Profile project.
Feel free to modify or extend them to suit your Discord server.
