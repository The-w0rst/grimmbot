import argparse
import asyncio
import os

from bots.grimbot import GrimBot
from bots.cursebot import CurseBot
from bots.bloombot import BloomBot

async def main() -> None:
    parser = argparse.ArgumentParser(description="Run multiple Discord bots")
    parser.add_argument("--grimbot-token", default=os.getenv("GRIMBOT_TOKEN"),
                        help="Token for GrimBot")
    parser.add_argument("--cursebot-token", default=os.getenv("CURSEBOT_TOKEN"),
                        help="Token for CurseBot")
    parser.add_argument("--bloombot-token", default=os.getenv("BLOOMBOT_TOKEN"),
                        help="Token for BloomBot")
    args = parser.parse_args()

    tasks = []
    if args.grimbot_token:
        tasks.append(GrimBot().start(args.grimbot_token))
    if args.cursebot_token:
        tasks.append(CurseBot().start(args.cursebot_token))
    if args.bloombot_token:
        tasks.append(BloomBot().start(args.bloombot_token))

    if not tasks:
        parser.error("At least one bot token must be provided")

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
