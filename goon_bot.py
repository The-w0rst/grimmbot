# Project repository: https://github.com/The-w0rst/grimmbot
import asyncio
import os
import glob
import logging
import discord
from discord.ext import commands
from pathlib import Path
from config.settings import load_config
from src.logger import setup_logging, log_message

setup_logging("goon_bot.log")
logger = logging.getLogger(__name__)

# Load a single shared configuration file for all bots
ENV_PATH = Path(__file__).resolve().parent / "config" / "setup.env"
if not ENV_PATH.exists():
    raise SystemExit("config/setup.env missing. Run 'python install.py' first.")
load_config({"DISCORD_TOKEN"})
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Allow '!', '*', and '?' prefixes like the individual bots


async def get_prefix(bot, message):
    prefixes = ["!", "*", "?"]
    return commands.when_mentioned_or(*prefixes)(bot, message)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)


@bot.event
async def on_ready():
    logger.info("Goon Bot online with cogs loaded.")
    log_message("Goon bot ready")


async def load_startup_cogs():
    for file in glob.glob("cogs/*_cog.py"):
        ext = f"cogs.{os.path.splitext(os.path.basename(file))[0]}"
        try:
            await bot.load_extension(ext)
            logger.info("Loaded %s", ext)
        except Exception as e:
            logger.warning("Failed to load %s: %s", ext, e)


asyncio.run(load_startup_cogs())

if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN not set in config/setup.env")
try:
    bot.run(DISCORD_TOKEN)
finally:
    log_message("Goon shutting down")
