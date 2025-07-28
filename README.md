# Grimmbot
Hey, it's **Curse** speaking. This repo holds me and my fellow goons. Grab it
from https://github.com/The-w0rst/grimmbot and run whichever of us you want.
We're lightweight, each in our own Python file. Fire up `goon_bot.py` if you
want the whole chaotic crew. It loads every cog and lets an Admin hot‑swap
modules whenever you feel like causing trouble.

## Repository layout

Here's what you'll find lurking in the repo:

- `grimm_bot.py` – Grimm is our cranky skeleton (prefix `!`).
- `bloom_bot.py` – Bloom brings bubbly chaos (prefix `*`).
- `curse_bot.py` – that's me, the mischievous calico (prefix `?`).
- `goon_bot.py` – pulls us all together as cogs.
- `config/setup.env` – one file to hold all the secret tokens.
- `requirements/base.txt` – packages the installer grabs.
- `bootstrap.sh` – one-liner to clone and run the setup.
- `install.py` – interactive installer for dependencies and config.
- `setup.sh` – optional helper for dependencies.
- `cogs/` – trivia, moderation, music, and other little toys.
- `media_player.py` – handles local tracks and links.

Every cog has a `COG_VERSION` constant. Keep an eye out for updates on the
`main` branch before merging your own tweaks.

## Installation

The fastest way is with the bootstrap script which handles everything for you:

```bash
bash <(curl -L https://raw.githubusercontent.com/The-w0rst/grimmbot/main/bootstrap.sh)
```

Prefer manual control? Follow these steps in your terminal:

1. Install **Python 3.10+**.
2. Clone the repo and enter the directory:

   ```bash
   git clone https://github.com/The-w0rst/grimmbot.git
   cd grimmbot
   ```
3. Install dependencies:

   ```bash
   python -m pip install -r requirements/base.txt
   ```
4. Run the installer to create `config/setup.env` and enter all your tokens and keys:

   ```bash
   python install.py
   ```
   Use `python configure.py` later if you need to update the file.
5. Start any bot you want:

   ```bash
   python grimm_bot.py   # or bloom_bot.py, curse_bot.py, goon_bot.py
   ```

For more nitty‑gritty steps check out [`INSTALL.md`](INSTALL.md).

## Running the bots

Once `config/setup.env` is filled in you can unleash any bot directly or through
the setup script:

```bash
python grimm_bot.py   # the cranky one
python bloom_bot.py   # the bubbly one
python curse_bot.py   # obviously the best one
python goon_bot.py    # load us all at once
python install.py     # reconfigure on the fly
```

GrimmBot can broadcast status to a Socket.IO dashboard if you define
`SOCKET_SERVER_URL` inside `config/setup.env`.

## Command reference

Here's a taste of what each bot can do.

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
- `!gloom` – check Grimm's gloom level.
- `!lament` – hear a gloomy thought.
- `!bonk [@user]` – bonk someone with a femur.
- `!inventory` – reveal a random item from Grimm's stash.
- `!shield [@user]` – provide mock protection.

### BloomBot
Commands use the `*` prefix:
- `*hug` – give a hug.
- `*sing` – burst into song.
- `*grimm` – talk about Grimm.
- `*curse` – tease Curse.
- `*cheer` – offer encouragement.
- `*sparkle` – throw confetti (and maybe cover you in glitter).
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
- `?curse @user` – manually curse a user (admin only).
- `?whois_cursed` – check the currently cursed user.
- `?sushi` – mention sushi.
- `?flick` – flick the tail.
- `?insult` – deliver an insult.
- `?hiss` – hiss at the server.
- `?scratch [@user]` – scratch someone just because.
- `?pet` – attempt to pet Curse (may end badly, or he might unleash a fent cloud).
- `?curse_me` – willingly take the curse.
- `?hairball` – share a revolting hairball.
- `?pounce [@user]` – pounce on someone unexpectedly.
- `?nap` – announce that Curse is taking a nap.

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

For every cog in detail check [`docs/cogs_overview.md`](docs/cogs_overview.md).

## Developing your own bots

Feeling creative? Peek at `goon_bot.py` for a modular design. It scans
`cogs/` at startup and you can load or unload them on the fly with the Admin
commands (`load`, `unload`, `reload`, `listcogs`).


## Example server layout

If you want to mimic our usual haunt, set up your server roughly like this.

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

An `AnnouncementCog` can shout reminders in `#gooning` and the `serverinfo`
command lists this layout in chat.
