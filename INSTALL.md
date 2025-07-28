# Goon Squad Bots - Installation Guide

Curse here. Let's get these bots running on your machine. This works on
Windows, macOS, or Linux—take your pick.

## Quick setup
1. Install Python 3.8 or newer.
2. Run the bootstrap script right from your terminal:
   ```bash
   bash <(curl -L https://raw.githubusercontent.com/The-w0rst/grimmbot/main/bootstrap.sh)
   ```
   That pulls down the repo, installs everything, and launches the interactive
   installer. Windows folks can use `py -3 install.py` instead if you clone
   manually.
3. When asked, toss in your Discord tokens and any API keys. You'll get a
   shiny `config/setup.env` file out of it.
4. Launch whichever bot you fancy:
   ```bash
   python grimm_bot.py   # or bloom_bot.py, curse_bot.py, goon_bot.py
   ```
   Windows users can replace `python` with `py -3`.

## Manual steps
Prefer to get your paws dirty?
1. Clone this repository:
   ```bash
   git clone https://github.com/The-w0rst/grimmbot.git
   cd grimmbot
   ```
2. Install the packages:
   ```bash
   pip install -r requirements/base.txt
   ```
   Optional developer extras are in `requirements/extra-dev.txt`.
3. Copy the environment template and fill it in:
   ```bash
   cp config/env_template.env config/setup.env
   ```
   On Windows use `copy` instead of `cp`. Fill in your Discord tokens and API
   keys.
4. Run any bot as shown above. All bots read from `config/setup.env`.

Place optional media files in the `localtracks` directory.
Cogs live under `cogs/` and can be customized or reloaded when using `goon_bot.py`.
