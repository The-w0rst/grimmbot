# Cogs Overview

This page gives a quick summary of each cog included with Grimmbot and the features it provides.

| Cog | Purpose |
| --- | ------- |
| `admin_cog.py` | Commands for loading, unloading and reloading other cogs at runtime. Owner only. |
| `announcement_cog.py` | Sends periodic announcements and exposes a `serverinfo` command describing the configured server layout. |
| `bloom_cog.py` | Implements the cheerful Bloom personality as a cog. |
| `curse_cog.py` | Implements the mischievous Curse personality. |
| `grimm_cog.py` | Implements the grumpy Grimm personality. |
| `fun_cog.py` | Provides quick games like dice rolls, coin flips and an 8‑ball. |
| `trivia_cog.py` | Simple trivia mini‑game. |
| `music_cog.py` | Stream audio from YouTube links into voice channels. |
| `moderation_cog.py` | Basic moderation commands (`kick`, `ban`, `clear`). |
| `gpt_cog.py` | ChatGPT based chat command and mention replies. Requires `OPENAI_API_KEY`. |
| `jojo_cog.py` | Sends loving messages to a user named "JoJo is bizarre". |
| `cyberpunk_campaign_cog.py` | Lightweight cyberpunk themed DnD campaign using ChatGPT. |

All cogs declare a `COG_VERSION` constant for easy tracking of updates. To load them individually see `goon_bot.py` or use the Admin cog commands.
