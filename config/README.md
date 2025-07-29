# Configuration Guide

Listen up, I'm **Curse**. Every bot sniffs out its tokens and API keys from one
file: `config/setup.env`. Keep it tidy and your secrets stay safe. Grab updates
at https://github.com/The-w0rst/grimmbot

## Creating `setup.env`

1. The easiest way is to run the interactive installer:

   ```bash
   python install.py
   ```
   It creates `config/setup.env` and walks you through each value with colorful prompts.

2. Prefer manual setup? Copy the template file:

   ```bash
   cp config/env_template.env config/setup.env
   ```

   Open `config/setup.env` and fill in all the tokens and keys. Sections are grouped by bot
(Grimm, Bloom, Curse) and shared settings. Add `OPENAI_API_KEY` for ChatGPT
features or `SOCKET_SERVER_URL` if you want status reporting.

### Environment variables

| Variable | Description |
| --- | --- |
| `GRIMM_DISCORD_TOKEN` | Discord bot token for Grimm |
| `GRIMM_API_KEY_1`-`GRIMM_API_KEY_3` | Custom API keys used by Grimm cogs |
| `GRIMM_OPENAI_KEY` | API key for Grimm's ChatGPT features |
| `GRIMM_GPT_ENABLED` | Toggle Grimm's ChatGPT commands |
| `SOCKET_SERVER_URL` | Optional Socket.IO status endpoint |
| `BLOOM_DISCORD_TOKEN` | Discord bot token for Bloom |
| `BLOOM_API_KEY_1`-`BLOOM_API_KEY_3` | API keys for Bloom-specific features |
| `BLOOM_OPENAI_KEY` | API key for Bloom's ChatGPT features |
| `BLOOM_GPT_ENABLED` | Toggle Bloom's ChatGPT commands |
| `CURSE_DISCORD_TOKEN` | Discord bot token for Curse |
| `CURSE_API_KEY_1`-`CURSE_API_KEY_3` | API keys for Curse's cogs |
| `CURSE_OPENAI_KEY` | API key for Curse's ChatGPT features |
| `CURSE_GPT_ENABLED` | Toggle Curse's ChatGPT commands |
| `DISCORD_TOKEN` | Token for the unified GoonBot |
| `OPENAI_API_KEY` | Enables GPT-based commands |

3. Save the file. Any bot you run will read these values automatically.

Do **not** commit `setup.env` to git. Keep it private.

Refer to [`../INSTALL.md`](../INSTALL.md) for instructions on installing the
required Python packages.
