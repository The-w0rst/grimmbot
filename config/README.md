# Configuration Guide

Listen up, I'm **Curse**. Every bot sniffs out its tokens and API keys from one
file: `config/setup.env`. Keep it tidy and your secrets stay safe. Grab updates
at https://github.com/The-w0rst/grimmbot

## Creating `setup.env`

1. The easiest way is to run the interactive installer:

   ```bash
   python install.py
   ```
   It'll create `config/setup.env` and nag you for each value.

2. Prefer manual setup? Copy the template file:

   ```bash
   cp config/env_template.env config/setup.env
   ```

   Open `config/setup.env` and fill everything in. Sections are grouped by bot
   (Grimm, Bloom, me) then shared settings. Add `OPENAI_API_KEY` for ChatGPT
   features or `SOCKET_SERVER_URL` if you want status reporting.

3. Save the file. Any bot you run will slurp up these values automatically.

Do **not** commit `setup.env` to git. Keep it private.

Refer to [`../INSTALL.md`](../INSTALL.md) for instructions on installing the
required Python packages.
