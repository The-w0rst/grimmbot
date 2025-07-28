# Goon Squad Bots - Installation Guide

Curse here. Let's get these bots running on your machine. This works on
Windows, macOS, or Linux—take your pick.

## Quick setup
1. Install Python 3.10 or newer.
2. Run the bootstrap script:
   ```bash
   bash <(curl -L https://raw.githubusercontent.com/The-w0rst/grimmbot/main/bootstrap.sh)
   ```
   It clones the repo, installs dependencies, and starts the installer. On Windows run `py -3 install.py` after cloning instead.
3. Enter your Discord tokens and API keys when prompted. They are saved to `config/setup.env`.
4. Start a bot of your choice:
   ```bash
   python grimm_bot.py   # or bloom_bot.py, curse_bot.py, goon_bot.py
   ```
   (Use `py -3` instead of `python` on Windows.)

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
4. Run `python install.py` to walk through the prompts.
5. Launch any bot as shown above. All bots read from `config/setup.env`.

Place optional media files in the `localtracks` directory.
Cogs live under `cogs/` and can be customized or reloaded when using `goon_bot.py`.
