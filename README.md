# Grimmbot

Grimmbot is a small collection of Discord bots that make up the "Goon Squad":
Grimm, Bloom and Curse. Each bot lives in its own Python file and has a
slightly different personality. The project is intentionally lightweight so you
can run one bot or all three depending on your needs. A new optional script
`goon_bot.py` automatically loads every personality from the `cogs/` folder and
includes an Admin cog for dynamically loading/unloading modules at runtime.
This mirrors the modular approach used by Red Discord Bot.

## Repository layout

- `grimm_bot.py` – GrimmBot, the grumpy skeleton leader (command prefix `!`).
- `bloom_bot.py` – BloomBot, cheerful chaos embodied (command prefix `*`).
- `curse_bot.py` – CurseBot, a mischievous calico (command prefix `!`).
- `goon_bot.py` – Unified bot that loads all personalities as cogs.
- `config/*.env` – Environment variables for each bot.
- `requirements.txt` – Python package requirements.
- `setup.sh` – Optional helper script for installing dependencies.
- `the-worst-grimbot/` – Old prototype code kept for reference.
- `cogs/trivia_cog.py` – Simple trivia mini‑game.
- `cogs/moderation_cog.py` – Basic kick/ban/clear commands.
- `cogs/music_cog.py` – Stream audio from YouTube links.

The `main` branch contains the latest working bots. New ideas or additional
robots can be developed on their own branches and merged back once stable.

## Setup

1. Ensure Python 3.8 or higher is installed.
2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   Alternatively you can run `./setup.sh` which installs the same
   dependencies for you.
3. Fill in the environment files found in `config/` with your Discord token and
   any API keys the bots rely on:

   - `config/grimm.env`
   - `config/bloom.env`
   - `config/curse.env`
   - `config/goon.env`

   Each file defines variables named like `GRIMM_DISCORD_TOKEN` or
   `BLOOM_API_KEY_1`. The example values show what to set.

## Running the bots

Each bot is completely independent. Activate the corresponding environment file
(or keep the variables in `.env` form) and launch the bot you want online:

```bash
python grimm_bot.py   # uses ! commands
python bloom_bot.py   # uses * commands
python curse_bot.py   # uses ! commands
python goon_bot.py    # loads all personalities with both prefixes
```

GrimmBot optionally reports its status to a Socket.IO dashboard if
`SOCKET_SERVER_URL` is set in `config/grimm.env`.

## Command reference

### GrimmBot
- `!protectbloom` – defend Bloom from imaginary threats.
- `!roast [@user]` – deliver a grumpy roast.
- `!goon` – call the goon squad.
- `!ominous` – send an ominous quip.
- `!bloom` – comments about Bloom.
- `!curse` – comments about Curse.
- `!scythe` – dramatic scythe swing.
- `!shadow` – send a spooky shadow.
- `!flip [@user]` – flip a user.
- `!brood` – quietly brood.
- `!bone` – offer a skeletal joke.
- `!shield [@user]` – provide mock protection.

### BloomBot
Commands use the `*` prefix:
- `*hug` – give a hug.
- `*sing` – burst into song.
- `*grimm` – talk about Grimm.
- `*curse` – tease Curse.
- `*cheer` – offer encouragement.
- `*sparkle` – throw confetti.
- `*drama` – start a musical.
- `*bloom` – introduce Bloom.
- `*mood` – display Bloom's mood.
- `*improv` – begin improv.
- `*squad` – list the goon squad.
- `*boba` – talk about bubble tea.
- `*compliment` – send a random compliment.

### CurseBot
- `!curse @user` – manually curse a user (admin only).
- `!whois_cursed` – check the currently cursed user.
- `!sushi` – mention sushi.
- `!flick` – flick the tail.
- `!insult` – deliver an insult.
- `!hiss` – hiss at the server.
- `!scratch [@user]` – scratch someone just because.
- `!curse_me` – willingly take the curse.

### Additional cogs
- `trivia` – play a quick trivia round.
- `kick/ban` – moderation commands restricted to users with the appropriate permissions.
- `clear` – remove a handful of recent messages.
- `play <url>` – stream music from YouTube into a voice channel.
- `stop` – stop music and disconnect from voice.

## Developing your own bots

The script `project_generator.sh` was once used to create prototype code inside
`the-worst-grimbot/`. Feel free to fork this repository or create a new branch
if you want to experiment with additional personalities.

For a modular approach similar to the Red Discord Bot, check out
`goon_bot.py`. It now scans the `cogs/` directory on startup and loads every
extension it finds. You can enable or disable cogs at runtime with the Admin
commands (`load`, `unload`, `reload`, and `listcogs`).

