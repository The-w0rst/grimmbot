# Configuration Guide

All bots read their tokens and API keys from a single file:
`config/setup.env`. Keeping everything in one place makes it easy to manage
credentials and avoids duplicating values across multiple files.

## Creating `setup.env`

1. The easiest way is to run the interactive installer:

   ```bash
   python install.py
   ```
   This will create `config/setup.env` and prompt for each value.

2. If you prefer manual setup, copy the template file:

   ```bash
   cp config/env_template.env config/setup.env
   ```

   Then open `config/setup.env` in your editor and fill in each value. The sections
   are grouped by bot (Grimm, Bloom, Curse) followed by shared settings. Set
   `OPENAI_API_KEY` if you want ChatGPT features. Optionally define
   `SOCKET_SERVER_URL` to enable status reporting to a Socket.IO dashboard.

3. Save the file. When you run any bot it automatically loads these values.

Do **not** commit `setup.env` to version control. It should remain private.

Refer to [`../INSTALL.txt`](../INSTALL.txt) for instructions on installing the
required Python packages.
