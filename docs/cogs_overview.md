# Cogs Overview

Curse here again. Here's a quick summary of each cog bundled with Grimmbot and
what mischief it adds. All cogs are currently **v2.0.1**.

| Cog | Purpose |
| --- | ------- |
| `admin_cog.py` | Commands for loading, unloading and reloading other cogs at runtime. Owner only. |
| `announcement_cog.py` | Sends periodic announcements and exposes a `serverinfo` command describing the configured server layout. |
| `bloom_cog.py` | Implements the cheerful Bloom personality with `*play` music commands and an EPIC musical trigger. |
| `curse_cog.py` | Implements the mischievous Curse personality. |
| `grimm_cog.py` | Implements the grumpy Grimm personality. |
| `grimm_extra_cog.py` | Extra utilities for Grimm: gloom meter, laments and bonks. |
| `fun_cog.py` | Provides quick games like dice rolls, coin flips and an 8‑ball. |
| `trivia_cog.py` | Simple trivia mini‑game. |
| `music_cog.py` | Queue YouTube links or playlists with basic controls. |
| `moderation_cog.py` | Basic moderation commands (`kick`, `ban`, `clear`). |
| `gpt_cog.py` | ChatGPT based chat command and mention replies. Requires `OPENAI_API_KEY`. |
| `cyberpunk_campaign_cog.py` | Lightweight cyberpunk themed DnD campaign using ChatGPT. See [cyberpunk_adventure.md](cyberpunk_adventure.md) for expanded scenarios. |
| `help_cog.py` | Provides `help` commands for each bot and a `helpall` summary. |
| `health_cog.py` | Shows a unified health menu for the squad. |
| `goon_cog.py` | The whole squad chiming in together. |
| `judge_cog.py` | Simple relationship judge that lets the squad weigh in via DM. |

All cogs declare a `COG_VERSION` constant for easy tracking of updates. Load them one by one with `goon_bot.py` or the Admin commands.
For music playback details see [`music_setup.md`](music_setup.md).
Happy gooning, - Curse
