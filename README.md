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
- `config/setup.env` – Environment variables for all bots in one place.
- `requirements.txt` – Python package requirements.
- `install.py` – Interactive installer for dependencies and config.
- `setup.sh` – Optional helper script for installing dependencies.
- `cogs/trivia_cog.py` – Simple trivia mini‑game.
- `cogs/moderation_cog.py` – Basic kick/ban/clear commands.
- `cogs/music_cog.py` – Stream audio from YouTube links.
- `cogs/fun_cog.py` – Quick games like dice rolls and an 8‑ball.
- `media_player.py` – Helpers for parsing media queries and local files.
- `media_player.is_supported_extension()` checks media file extensions.
- Each cog now declares `COG_VERSION` for easy tracking of updates.
- Each personality gives out a small daily gift if the bot stays online.
- `INSTALL.md` – cross-platform installation instructions.

The `main` branch contains the latest working bots. New ideas or additional
robots can be developed on their own branches and merged back once stable.

## Quick setup

1. Install Python 3.8 or newer.
2. Run the interactive installer which guides you through installing
   dependencies and creating `config/setup.env`:

   ```bash
   python install.py
   ```

   The installer walks you through each required value. You can rerun it at
   any time to update the configuration. Set `OPENAI_API_KEY` if you want
   ChatGPT powered features. See

   [`config/README.md`](config/README.md) provides a line-by-line explanation.

For a step-by-step installation guide see [`INSTALL.md`](INSTALL.md).

## Running the bots

Each bot is completely independent. As long as `config/setup.env` is populated
with your credentials you can launch any bot directly or via the setup script:

```bash
python grimm_bot.py   # uses ! commands
python bloom_bot.py   # uses * commands
python curse_bot.py   # uses ! commands
python goon_bot.py    # loads all personalities with both prefixes
python install.py     # optional installer with launch option
```

GrimmBot optionally reports its status to a Socket.IO dashboard if
`SOCKET_SERVER_URL` is defined in `config/setup.env`.

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
- `*boy` – share a playful boy-themed line.
- `*queen` – share a playful "yas queen" line.

### CurseBot
- `!curse @user` – manually curse a user (admin only).
- `!whois_cursed` – check the currently cursed user.
- `!sushi` – mention sushi.
- `!flick` – flick the tail.
- `!insult` – deliver an insult.
- `!hiss` – hiss at the server.
- `!scratch [@user]` – scratch someone just because.
- `!pet` – attempt to pet Curse (may end badly).
- `!curse_me` – willingly take the curse.

### Additional cogs
- `trivia` – play a quick trivia round.
- `kick/ban` – moderation commands restricted to users with the appropriate permissions.
- `clear` – remove a handful of recent messages.
- `play <url>` – stream music from YouTube into a voice channel.
- `stop` – stop music and disconnect from voice.
- `chat <prompt>` – ask ChatGPT a question and get an in-character reply.
- `roll [sides]` – roll a dice with an optional number of sides.
- `8ball <question>` – consult the magic 8-ball.
- `coinflip` – flip a coin.
- `quote` – receive a random motivational quote.
- `jojo` – shower Emma ("JoJo is bizarre") with affection.
- `cyberstart` – begin a cyberpunk themed DnD campaign.
- `cyberfight` – fight one of the bots with evolving difficulty.
- `cyberstatus` – view your campaign record.
- `cyberchat <prompt>` – talk to the campaign's narrator and characters via ChatGPT.

## Developing your own bots

For a modular approach similar to the Red Discord Bot, check out
`goon_bot.py`. It now scans the `cogs/` directory on startup and loads every
extension it finds. You can enable or disable cogs at runtime with the Admin
commands (`load`, `unload`, `reload`, and `listcogs`).


## Example server layout

These bots were designed with the following Discord server structure in mind.

### Roles
- Server booster
- Goons
- Goonets
- Royalty

### Categories and channels
- **Intake**: `#new-here`
- **Gen pop**: `#non-gooning`, `#gooning`
- **Yapping**: `yapper's anonymous` (voice)
- **Royalty**: `#me-n-bea`, `the-baby-yap` (voice)

An `AnnouncementCog` periodically posts reminders in `#gooning` and provides a
`serverinfo` command that lists this layout in chat.
