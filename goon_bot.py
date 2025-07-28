import asyncio
import os
import glob
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

# Load a single shared configuration file for all bots
ENV_PATH = Path(__file__).resolve().parent / "config" / "setup.env"
load_dotenv(ENV_PATH)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Allow both '!' and '*' prefixes like the individual bots


async def get_prefix(bot, message):
    prefixes = ['!', '*']
    return commands.when_mentioned_or(*prefixes)(bot, message)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents)


@bot.event
async def on_ready():
    print("Goon Bot online with cogs loaded.")


async def load_startup_cogs():
    for file in glob.glob("cogs/*_cog.py"):
        ext = f"cogs.{os.path.splitext(os.path.basename(file))[0]}"
        try:
            await bot.load_extension(ext)
            print(f"Loaded {ext}")
        except Exception as e:
            print(f"Failed to load {ext}: {e}")

asyncio.run(load_startup_cogs())

if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN not set in config/setup.env")
bot.run(DISCORD_TOKEN)
