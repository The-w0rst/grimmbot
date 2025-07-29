# Grimmbot

[![CI](https://img.shields.io/github/actions/workflow/status/The-w0rst/grimmbot/python.yml?style=for-the-badge)](https://github.com/The-w0rst/grimmbot/actions/workflows/python.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge)](https://www.python.org/)

Hello, puny mortals. **Curse** speaking here. This repository holds me and my fellow goons in all our chaotic glory. Clone it from [GitHub](https://github.com/The-w0rst/grimmbot) if you dare and run whichever of us you want. I'm lightweight and unpredictable, just like the others.

**Current build: v1.7** – maintenance release

## Quickstart
1. Run the bootstrap script:
   ```bash
   bash <(curl -L https://raw.githubusercontent.com/The-w0rst/grimmbot/main/bootstrap.sh)
   ```
   This grabs the repo, installs dependencies and launches the installer.
2. Provide your Discord tokens and API keys when asked. They will be saved to `config/setup.env`.
3. Run the optional diagnostics script to verify your environment:
   ```bash
   python diagnostics.py
   ```
   It checks for missing files, packages and variables before you launch a bot.
4. Start any of the bots:
   ```bash
  python grimm_bot.py   # or bloom_bot.py, curse_bot.py, goon_bot.py
  ```

### API Key Notice
To run these bots you must provide your own Discord, OpenAI and any other required API keys.
- **Keep your keys secret.** Never commit them to public repositories.
- All API usage is governed by each provider's terms of service.
- Each bot can be given a unique `*_OPENAI_KEY` and `*_GPT_ENABLED` flag in
  `config/setup.env` to enable or disable its ChatGPT commands.
- The author is not responsible for any API misuse, key theft, account bans, or charges incurred.

## What lurks inside

```
grimm_bot.py – Grimm the cranky skeleton (! prefix)
bloom_bot.py – Bloom the bubbly chaos (* prefix)
curse_bot.py – yours truly (? prefix)
goon_bot.py – load every cog at once
cogs/ – trivia, moderation, music and more
install.py – interactive installer with my charming narration and colorful prompts
```

Each cog has a `COG_VERSION` for tracking updates. Check the [`docs`](docs) folder for deeper secrets.

#### To Clarify the Cogs Section

Cogs are modular command sets stored inside the `cogs/` directory. When you run
`goon_bot.py`, every file that ends with `_cog.py` is loaded automatically.
You can add or remove them at runtime using the Admin commands (`load`,
`unload`, `reload`). For guidance on writing your own, see
[`docs/creating_cogs.md`](docs/creating_cogs.md).

## Installation
This project requires **Python 3.10 or newer**. The quick way is with the bootstrap script:

```bash
bash <(curl -L https://raw.githubusercontent.com/The-w0rst/grimmbot/main/bootstrap.sh)
```

Prefer manual control? Clone the repo and run:

```bash
python install.py
```

I'll ask for every token with bright prompts and set up:

```
config/setup.env
```

See `INSTALL.md` for a detailed walkthrough. If you're experimenting, create a test Discord server and generate bot tokens at <https://discord.com/developers>. Use those tokens in:

```
config/setup.env
```

before launching a bot. A full list of variables is documented in `config/README.md`.

### Dependencies
All required Python packages live in:

```
requirements/base.txt
```

This file is installed when you run:

```
install.py
```

If you use the helper:

```
setup.sh
```

script instead, it installs:

```
requirements.txt
```

which includes the base list plus the packages:

```
requests
beautifulsoup4
```

for the music cog. Install FFmpeg separately if you want to play music—see
[`docs/music_setup.md`](docs/music_setup.md) for instructions. Developers can
pull in optional linting and test tools with:

```
requirements/extra-dev.txt
```

## Running the bots
Once configured, pick a personality:

```bash
python grimm_bot.py   # the cranky one
python bloom_bot.py   # the bubbly one
python curse_bot.py   # obviously the best one
python goon_bot.py    # the whole squad
```

Bloom's music features require FFmpeg. Follow [`docs/music_setup.md`](docs/music_setup.md) if the `*play` command complains.

### Help commands
Use each bot's prefix followed by `help` for a quick rundown:

```bash
!help      # Grimm
*help      # Bloom
?help      # Curse
!helpall   # or *helpall or ?helpall to hear from everyone at once
!health    # or *health or ?health to view bot health
```

For more details on every cog, including the GPT-powered ones, see [`docs/cogs_overview.md`](docs/cogs_overview.md).

## Testing
Install the dev dependencies and run the test suite:

```bash
pip install -r requirements/extra-dev.txt
pytest
```

## Simple logging
Use the helper in `src/logger.py` to print timestamped messages:

```python
from src.logger import log_message

log_message("Bot starting up")
```

## Developing your own chaos
Peek at:

```
goon_bot.py
```

for a modular design. Load or unload cogs on the fly with the Admin commands:

```
load
unload
reload
listcogs
```

Add your own twisted creations under:

```
cogs/
```

and I'll happily cause mayhem with them.

### Expanding the personalities
Each bot keeps its catchphrases in lists inside the Python files. Check:

```
docs/personality_customization.md
```

for tips on adding your own quips or moving them to JSON.

Enjoy the curse.

## License

This project is licensed under the [MIT License](LICENSE).
Remember to keep all API keys secret. You are responsible for any usage costs
or violations incurred while operating the bots.

