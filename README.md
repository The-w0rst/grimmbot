# Grimmbot Repository

This repository uses `main` as the primary branch. Any new work should branch
from `main` and later merge back into it.

Individual robots are expected to be developed on their own branches. Example
branch names could be:

- `alpha-robot`
- `beta-robot`
- `gamma-robot`

Each robot branch contains its own `setup.exe` installer. To work on a specific
robot, check out its branch and run the installer:

```bash
git checkout <robot-branch>
./setup.exe
```

These branches and the installers are placeholders and may not be available in
this repository yet.

## Setup

Run `./setup.exe` to install dependencies. Configuration files for API keys and
tokens live in the `config/` directory:

- `config/grimm.env`
- `config/bloom.env`
- `config/curse.env`

Fill in each file with the three API keys and Discord token for its bot before
starting the bots.

## Running the Bots

After configuring the `.env` files, launch a bot with Python:

```bash
python grimm_bot.py    # prefix: !
python bloom_bot.py    # prefix: *
python curse_bot.py    # prefix: !
```

## Command Reference

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

### CurseBot
- `!curse @user` – manually curse a user (admin only).
- `!whois_cursed` – check the currently cursed user.
- `!sushi` – mention sushi.
- `!flick` – flick the tail.
- `!insult` – deliver an insult.

