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
3. Run the installer and hand over your Discord tokens and API keys when Curse asks. They are saved to `config/setup.env`.
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
4. Run `python install.py` and follow Curse's friendly prompts.
   The installer guides you through four steps:
   1. **Python check** – verifies you're running Python 3.10 or newer.
   2. **Dependencies** – when asked `Install dependencies now? [Y/n]` press
      Enter to install from `requirements/base.txt` or type `n` to skip.
   3. **Configuration** – you'll be prompted for each value listed in
      `config/env_template.env`:
      - `GRIMM_DISCORD_TOKEN`
      - `GRIMM_API_KEY_1`
      - `GRIMM_API_KEY_2`
      - `GRIMM_API_KEY_3`
      - `SOCKET_SERVER_URL` *(optional)*
      - `BLOOM_DISCORD_TOKEN`
      - `BLOOM_API_KEY_1`
      - `BLOOM_API_KEY_2`
      - `BLOOM_API_KEY_3`
      - `CURSE_DISCORD_TOKEN`
      - `CURSE_API_KEY_1`
      - `CURSE_API_KEY_2`
      - `CURSE_API_KEY_3`
      - `DISCORD_TOKEN`
      - `OPENAI_API_KEY`
      Leave a value blank to keep any existing entry.
   4. **Choose bot** – finally you'll see a menu:
      `1. GrimmBot`, `2. BloomBot`, `3. CurseBot`, `4. GoonBot`, `0. Exit`.
      Enter a number to launch a bot immediately or `0` to finish without
      starting one.
5. Launch any bot as shown above. All bots read from `config/setup.env`.

Place optional media files in the `localtracks` directory.
Cogs live under `cogs/` and can be customized or reloaded when using `goon_bot.py`.
