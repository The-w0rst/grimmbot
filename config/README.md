# Configuration Guide

All bots read their tokens and API keys from a single file:
`config/setup.env`. Keeping everything in one place makes it easy to manage
credentials and avoids duplicating values across multiple files.

## Creating `setup.env`

1. Copy the template file:

   ```bash
   cp config/env_template.env config/setup.env
   ```

2. Open `config/setup.env` in your editor and fill in each value. The sections
   are grouped by bot (Grimm, Bloom, Curse) followed by shared settings. Set
   `OPENAI_API_KEY` if you want ChatGPT features.

3. Save the file. When you run any bot it automatically loads these values.

Do **not** commit `setup.env` to version control. It should remain private.

Refer to [`../INSTALL.txt`](../INSTALL.txt) for instructions on installing the
required Python packages.
