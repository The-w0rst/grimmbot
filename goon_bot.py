import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from cogs.grimm_cog import GrimmCog
from cogs.bloom_cog import BloomCog
from cogs.curse_cog import CurseCog

# Load environment for the unified bot
load_dotenv("config/goon.env")
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

# Load cogs
bot.add_cog(GrimmCog(bot))
bot.add_cog(BloomCog(bot))
bot.add_cog(CurseCog(bot))

bot.run(DISCORD_TOKEN)
