################################################################################
#                                                                              #
#      ╔═╗┬─┐┬ ┬┌┐┌┌┐┌                                                        #
#      ║ ║├┬┘│ │││││││                                                        #
#      ╚═╝┴└─└─┘┘└┘┘└┘                                                        #
#                                                                              #
#      GrimmBot: The grumpy skeleton of the Goon Squad.                       #
#      Gruff, protective, secretly soft on the inside.                        #
#                                                                              #
################################################################################

import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("GRIMM_DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="#", intents=intents)

# === Grimm Personality ===
grimm_personality = {
    "name": "Grimm",
    "role": "leader",
    "traits": [
        "gruff",
        "sarcastic",
        "protective",
        "secretly soft",
        "tired of chaos"
    ],
    "companions": ["Bloom", "Curse"]
}

# === Random Grimm Responses ===
grimm_responses = [
    "What now?",
    "I'm not angry, just disappointed... again.",
    "Keep it down. I'm trying to brood.",
    "Don't tell Bloom, but I'm glad you're here.",
    "Curse, stop clawing the furniture.",
    "Sigh. Another day, another bit of chaos."
]

# === Keyword Triggers ===
keywords = {
    "bloom": [
        "She's all sunshine and noise.",
        "Bloom means well, I guess."
    ],
    "curse": [
        "That cat is trouble on four paws.",
        "Curse, put the sushi down."
    ],
    "grimm": [
        "That's me. What of it?",
        "Yes, yes, I'm the spooky one."
    ]
}

# === On Ready ===
@bot.event
async def on_ready():
    print(f"{grimm_personality['name']} has awakened and watches over the server.")

# === Message Handler ===
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    lowered = message.content.lower()
    for trigger, responses in keywords.items():
        if trigger in lowered:
            await message.channel.send(random.choice(responses))
            return
    if random.random() < 0.05:
        await message.channel.send(random.choice(grimm_responses))
    await bot.process_commands(message)

# === Commands ===
@bot.command()
async def brood(ctx):
    await ctx.send("*broods quietly in a dark corner*")

@bot.command()
async def bone(ctx):
    await ctx.send("You want a bone? I'm using all of mine.")

@bot.command()
async def bloom(ctx):
    await ctx.send("Bloom is probably off singing somewhere.")

@bot.command()
async def curse(ctx):
    await ctx.send("That cat's up to no good again.")

bot.run(DISCORD_TOKEN)
