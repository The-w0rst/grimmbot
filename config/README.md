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

3. For automated environments you can generate the file from existing shell
   variables:

   ```bash
   python generate_env.py
   ```

   Each entry in the template is filled with the matching environment variable.

### Environment variables

| Variable | Description |
| --- | --- |
| `GRIMM_DISCORD_TOKEN` | Discord bot token for Grimm |
| `GRIMM_API_KEY_1`-`GRIMM_API_KEY_3` | OpenAI keys used by Grimm |
| `GRIMM_GPT_ENABLED` | Toggle Grimm's ChatGPT commands |
| `SOCKET_SERVER_URL` | Optional Socket.IO status endpoint |
| `BLOOM_DISCORD_TOKEN` | Discord bot token for Bloom |
| `BLOOM_API_KEY_1`-`BLOOM_API_KEY_3` | OpenAI keys used by Bloom |
| `BLOOM_GPT_ENABLED` | Toggle Bloom's ChatGPT commands |
| `CURSE_DISCORD_TOKEN` | Discord bot token for Curse |
| `CURSE_API_KEY_1`-`CURSE_API_KEY_3` | OpenAI keys used by Curse |
| `CURSE_GPT_ENABLED` | Toggle Curse's ChatGPT commands |
| `DISCORD_TOKEN` | Token for the unified GoonBot |
| `OPENAI_API_KEY` | Enables GPT-based commands |
| `SPOTIFY_CLIENT_ID` | Client ID for Spotify API searches |
| `SPOTIFY_CLIENT_SECRET` | Client secret for Spotify API searches |

3. Save the file. Any bot you run will read these values automatically.

Bots load related API keys in a single call using `get_env_vars` from
`config.settings` for cleaner code.

Do **not** commit `setup.env` to git. Keep it private.

Refer to [`../INSTALL.md`](../INSTALL.md) for instructions on installing the
required Python packages.
