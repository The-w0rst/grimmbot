# Goon Squad Bots - Installation Guide

This single document covers Windows, macOS and Linux.

## Quick setup
1. Install Python 3.8 or newer.
2. From a terminal, run:
   ```bash
   python install.py
   ```
   On Windows you may prefer `py -3 install.py`.
   The installer installs dependencies and creates `config/setup.env`.
3. Launch a bot:
   ```bash
   python grimm_bot.py   # or bloom_bot.py, curse_bot.py, goon_bot.py
   ```
   Again Windows users can replace `python` with `py -3`.

## Manual steps
If you wish to perform the setup yourself:
1. Install packages:
   ```bash
   pip install -r requirements/base.txt
   ```
   Optional developer extras are in `requirements/extra-dev.txt`.
2. Copy the environment template and edit it:
   ```bash
   cp config/env_template.env config/setup.env
   ```
   On Windows use `copy` instead of `cp`.
   Fill in your Discord tokens and API keys.
3. Run any bot as shown above. All bots read from `config/setup.env`.

Place optional media files in the `localtracks` directory.
Cogs live under `cogs/` and can be customized or reloaded when using `goon_bot.py`.
