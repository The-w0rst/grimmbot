# 💀💀💀

## Curse's Introduction

Hey there, mortals. It's **Curse**, your favorite chaotic cat, here to walk you through setting up the whole Grimmbot gang. Follow these steps and you'll have Grimm, Bloom, and me running in no time.

### Quick Setup
1. Install Python 3.10 or newer.
2. Run the bootstrap script directly:
   ```bash
   bash <(curl -L https://raw.githubusercontent.com/The-w0rst/grimmbot/main/bootstrap.sh)
   ```
   This grabs the code, installs everything, and launches the installer.
3. When the installer asks, enter your Discord tokens and API keys. A file called `config/setup.env` will appear with your secrets.
4. Launch any bot you want:
   ```bash
   python grimm_bot.py   # or bloom_bot.py, curse_bot.py, goon_bot.py
   ```

### Manual Setup
Prefer to do things yourself? Fine.
1. Clone the repo and jump in:
   ```bash
   git clone https://github.com/The-w0rst/grimmbot.git
   cd grimmbot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements/base.txt
   ```
3. Copy the environment template and fill in your tokens:
   ```bash
   cp config/env_template.env config/setup.env
   ```
4. Run `python install.py` to fill in the file interactively, or edit it manually.
5. Launch any of the bot files above and you're done.

Enjoy the chaos, courtesy of yours truly.
