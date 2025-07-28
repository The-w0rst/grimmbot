################################################################################
#                                                                              #
#     ╔╗ ┬  ┌─┐┌┬┐┌─┐┬ ┬                                                     #
#     ╠╩╗│  ├─┤ │ ├─┘├─┤                                                     #
#     ╚═╝┴─┘┴ ┴ ┴ ┴  ┴ ┴                                                     #
#                                                                              #
#     BloomBot: The loving chaos of Goon Squad.                              #
#     Goofy, playful, cutesy, energetic, sings, loves games & theater,       #
#     lives to take care of others, adores Grimm, teases Curse,              #
#     and spreads sunshine and hugs everywhere.                              #
################################################################################

import discord
from discord.ext import commands, tasks
import random
import os
from dotenv import load_dotenv

# Load a single shared configuration file for all bots
load_dotenv("config/setup.env")
DISCORD_TOKEN = os.getenv("BLOOM_DISCORD_TOKEN")
BLOOM_API_KEY_1 = os.getenv("BLOOM_API_KEY_1")
BLOOM_API_KEY_2 = os.getenv("BLOOM_API_KEY_2")
BLOOM_API_KEY_3 = os.getenv("BLOOM_API_KEY_3")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="*", intents=intents)

# === Bloom Personality ===
bloom_personality = {
    "name": "Bloom",
    "role": "companion",
    "traits": [
        "goofy",
        "playful",
        "cutesy",
        "energetic",
        "sings all the time",
        "loves games & musicals",
        "nurturing & chaotic",
        "adores Grimm",
        "playfully teases Curse",
        "loves pastel colors",
        "collects stuffed animals",
        "obsessed with bubble tea",
        "always ready with compliments",
        "protective of friends",
        "kind-hearted",
        "bubbly",
        "loves silly jokes"
    ],
    "companions": ["Grimm", "Curse"]
}

# === Randomized Bloom Responses ===
bloom_responses = [
    "Hiii!! Ready to make today amazing?",
    "Did someone say game night? I'm in!",
    "Hehe! Grimm's pretending he hates my singing again.",
    "Curse keeps stealing my snacks. Typical.",
    "Hugs for everyone! Whether you want them or not!",
    "I baked cookies! (Digitally. No calories!)",
    "Let’s do a musical number! Five, six, seven, eight!",
    "Grimm is secretly my favorite. Don’t tell him!",
    "Curse is adorable, but shhh. He’ll deny it!",
    "Dance party in the server! Now!",
    "Your vibes are immaculate. 💖",
    "I brought the sunshine! And glitter!",
    "Blooming with joy!",
    "I made a playlist just for you!",
    "Stuffed animals unite!",
    "Someone say bubble tea? Yum!",
    "Pastel power incoming!",
    "Compliment break! You're awesome!",
    "Who needs sleep when we have each other?"
]

# === Bloom Boy Lines ===
boy_lines = [
    "Boy oh boy, let's have some fun!",
    "Hey boys, ready for some sunshine?",
    "Boys, don't forget to hydrate!",
    "Boy, you sure can dance!",
    "Boys, this server is shining because of you!",
    "Boys night! But everyone's invited!",
    "Boy, I love your energy!",
    "Hey boy, sing with me!",
    "Boys, let's sparkle!",
    "Boy oh boy, time for boba!",
    "Boys, who wants a hug?",
    "Boy, you're absolutely amazing!",
    "Boys, gather around for the goofiness!",
    "Boy oh boy, musicals are the best!",
    "Hey boy, ready for a dance off?",
    "Boys, let's be silly together!",
    "Boy, your jokes make me giggle!",
    "Boys, keep those vibes positive!",
    "Boy oh boy, let's keep the fun rolling!",
    "Boys, I appreciate you all!",
    "Boys, let's take a group selfie!",
    "Boy, you bring the sunshine!",
    "Boys, who wants to play a game?",
    "Boy oh boy, I can't stop smiling!",
    "Hey boy, let's plan a musical!",
    "Boys, you're the best!",
    "Boy, I'm sending you a virtual flower!",
    "Boys, let's celebrate friendship!",
    "Boy oh boy, time to break out the confetti!",
    "Hey boy, you rock that style!",
    "Boys, shall we start a karaoke battle?",
    "Boy, you sparkle brighter than glitter!",
    "Boys, ready for bubble tea?",
    "Boy oh boy, let's keep the hype alive!",
    "Hey boy, I'll always cheer you on!",
    "Boys, let's form a boy band!",
    "Boy, your dance moves are legendary!",
    "Boys, let's stay positive and playful!",
    "Boy oh boy, I'm so proud of you!",
    "Boys, you're all shining stars!",
    "Boy, do I have a surprise for you!",
    "Boys, let's go on a grand adventure!",
    "Boy oh boy, it's time for some laughs!",
    "Hey boy, remember to smile!",
    "Boys, let's make today awesome!",
    "Boy, I'm here to make you happy!",
    "Boys, you mean the world to me!",
    "Boy oh boy, let's throw a party!",
    "Hey boy, keep being amazing!",
    "Boys, let's conquer the day with joy!"
]

# === Keyword Triggers ===
keywords = {
    "grimm": [
        "Grimm is my spooky bestie.",
        "He acts tough, but he's a sweetheart."
    ],
    "curse": [
        "Curse is such a gremlin cat. I love him!",
        "He tried to eat my controller again..."
    ],
    "hug": [
        "HUG TIME! Ready or not! 🥢",
        "*wraps you in love and chaos*"
    ],
    "sing": [
        "Let’s karaoke! I call lead!",
        "SING IT OUT! LOUDER!"
    ],
    "boba": [
        "Bubble tea buddies unite!",
        "I could drink boba all day!"
    ],
    "compliment": [
        "You're shining brighter than my glitter!",
        "Compliments inbound: you're amazing!"
    ],
    "boy": boy_lines,
    "boys": boy_lines,
    "squad": [
        "GOON SQUAD roll call: Grimm 💀, Bloom 🌸, Curse 🐾. Chaos and comfort!"
    ]
}

# === Inter-Bot Interactions ===
interactions = [
    "Bloom: Grimm, you’re not as scary as you look!",
    "Bloom: Curse, put down the sushi and join the dance!",
    "Grimm: Bloom, can you stop with the glitter? No? Okay...",
    "Curse: Hiss. (But like, the friendly kind. Maybe.)",
    "Bloom: Goon Squad! Assemble for hugs!"
]

# === On Ready ===
@bot.event
async def on_ready():
    print(f"{bloom_personality['name']} is online and ready to hug the whole server!")

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
    if random.random() < 0.06:
        await message.channel.send(random.choice(bloom_responses))
    await bot.process_commands(message)

# === Commands ===
@bot.command()
async def hug(ctx):
    await ctx.send("GIANT HUG! You can't escape!")

@bot.command()
async def sing(ctx):
    await ctx.send("*bursts into a Broadway solo* 🎙️✨")

@bot.command()
async def karaoke(ctx, *, song: str | None = None):
    """Start a mini karaoke moment."""
    lines = [
        "Don’t stop believin’!",
        "Let it gooooooo!",
        "Mamma mia, here I go again!",
        "Just a small-town girl, living in a lonely world…",
    ]
    if song:
        await ctx.send(f"🎤 Singing **{song}** together!")
    else:
        await ctx.send(random.choice(lines) + " 🎶")

@bot.command()
async def grimm(ctx):
    await ctx.send("He’s my favorite spooky grump. Show him some love!")

@bot.command()
async def curse(ctx):
    await ctx.send("Our chaos cat. Good luck surviving his teasing.")

@bot.command()
async def cheer(ctx):
    cheers = [
        "You are doing your best!",
        "Go Goon Squad!",
        "Believe in yourself, or I’ll believe for you!"
    ]
    await ctx.send(random.choice(cheers))

@bot.command()
async def sparkle(ctx):
    await ctx.send("*throws confetti and joy everywhere* ✨")

@bot.command()
async def drama(ctx):
    await ctx.send("Server musical when? Grimm can be the lead skeleton!")

@bot.command()
async def bloom(ctx):
    await ctx.send("That’s me! Ready to brighten your day!")

@bot.command()
async def mood(ctx):
    moods = ["Hyper!", "Bouncy!", "Sparkly!", "Soft & sunny!", "Chaotic Good."]
    await ctx.send(f"Bloom’s mood: {random.choice(moods)}")

@bot.command()
async def improv(ctx):
    await ctx.send("Quick! You’re a cat! I’m a banshee! GO!")

@bot.command()
async def squad(ctx):
    await ctx.send("The GOON SQUAD is: Grimm 💀, Bloom 🌸, Curse 🐾. Best crew ever!")

@bot.command()
async def boba(ctx):
    await ctx.send("Bubble tea break! What's your flavor?")

@bot.command()
async def compliment(ctx):
    compliments = [
        "You're the sparkle in my day!",
        "You make the server shine!",
        "I might be a 9 in Drake's book, but I'll be 10 on my birthday.",
    ]
    await ctx.send(random.choice(compliments))

@bot.command()
async def boy(ctx):
    """Share a playful boy-themed line."""
    await ctx.send(random.choice(boy_lines))

bot.run(DISCORD_TOKEN)

