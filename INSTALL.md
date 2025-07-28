# Goon Squad Bots - Installation Guide

This single document covers Windows, macOS and Linux.

## Quick setup
1. Install Python 3.8 or newer.
2. Run the bootstrap script directly from your terminal:
   ```bash
   bash <(curl -L https://raw.githubusercontent.com/The-w0rst/grimmbot/main/bootstrap.sh)
   ```
   This clones the repository, installs dependencies and launches the
   interactive installer. On Windows you may prefer `py -3 install.py`
   after cloning manually.
3. When prompted, enter your Discord tokens and any API keys. A file
   `config/setup.env` will be created.
4. Launch a bot:
   ```bash
   python grimm_bot.py   # or bloom_bot.py, curse_bot.py, goon_bot.py
   ```
   Again Windows users can replace `python` with `py -3`.

## Manual steps
If you wish to perform the setup yourself:
1. Clone this repository:
   ```bash
   git clone https://github.com/The-w0rst/grimmbot.git
   cd grimmbot
   ```
2. Install packages:
   ```bash
   pip install -r requirements/base.txt
   ```
   Optional developer extras are in `requirements/extra-dev.txt`.
3. Copy the environment template and edit it:
   ```bash
   cp config/env_template.env config/setup.env
   ```
   On Windows use `copy` instead of `cp`.
   Fill in your Discord tokens and API keys.
4. Run any bot as shown above. All bots read from `config/setup.env`.

Place optional media files in the `localtracks` directory.
Cogs live under `cogs/` and can be customized or reloaded when using `goon_bot.py`.
