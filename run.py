"""Entry point to launch one of the Discord bots."""

import os
import argparse

from bots.grimbot import GrimBot
from bots.cursebot import CurseBot
from bots.bloombot import BloomBot


BOTS = {
    "grimbot": GrimBot,
    "cursebot": CurseBot,
    "bloombot": BloomBot,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a Discord bot")
    parser.add_argument(
        "bot",
        choices=BOTS.keys(),
        help="Which bot to run (grimbot, cursebot, bloombot)",
    )
    parser.add_argument(
        "--token",
        help="Discord bot token. Can also be provided via DISCORD_TOKEN env var",
    )
    args = parser.parse_args()

    token = args.token or os.environ.get("DISCORD_TOKEN")
    if not token:
        raise SystemExit("A Discord token must be provided via --token or DISCORD_TOKEN env var")

    bot_cls = BOTS[args.bot]
    bot = bot_cls()
    bot.run(token)


if __name__ == "__main__":
    main()
