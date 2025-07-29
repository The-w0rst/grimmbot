# Grimmbot

Hello, puny mortals. **Curse** speaking here. This repository holds me and my fellow goons in all our chaotic glory. Clone it from [GitHub](https://github.com/The-w0rst/grimmbot) if you dare and run whichever of us you want. I'm lightweight and unpredictable, just like the others.

**Current build: v1.4** – first public release

## What lurks inside
- `grimm_bot.py` – Grimm the cranky skeleton (`!` prefix)
- `bloom_bot.py` – Bloom the bubbly chaos (`*` prefix)
- `curse_bot.py` – yours truly (`?` prefix)
- `goon_bot.py` – load every cog at once
- `cogs/` – trivia, moderation, music and more
- `install.py` – interactive installer with my charming narration

Each cog has a `COG_VERSION` for tracking updates. Check the [`docs`](docs) folder for deeper secrets.

## Installation
The quick way is with the bootstrap script:

```bash
bash <(curl -L https://raw.githubusercontent.com/The-w0rst/grimmbot/main/bootstrap.sh)
```

Prefer manual control? Clone the repo and run `python install.py`. I'll ask for every token and set up `config/setup.env` for you. See [INSTALL.md](INSTALL.md) for a detailed walkthrough.

## Running the bots
Once configured, pick a personality:

```bash
python grimm_bot.py   # the cranky one
python bloom_bot.py   # the bubbly one
python curse_bot.py   # obviously the best one
python goon_bot.py    # the whole squad
```

### Help commands
Use each bot's prefix followed by `help` for a quick rundown:

- `!help` for Grimm
- `*help` for Bloom
- `?help` for Curse
- `!helpall` or `*helpall` or `?helpall` to hear from everyone at once

For more details on each cog see [`docs/cogs_overview.md`](docs/cogs_overview.md).

## Developing your own chaos
Peek at `goon_bot.py` for a modular design. Load or unload cogs on the fly with the Admin commands (`load`, `unload`, `reload`, `listcogs`). Add your own twisted creations under `cogs/` and I'll happily cause mayhem with them.

Enjoy the curse.
