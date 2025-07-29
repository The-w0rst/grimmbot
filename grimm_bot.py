###############################################################################
#
#
#      ╔═╗┬─┐┬ ┬┌┐┌┌┐┌                                                        #
#      ║ ║├┬┘│ │││││││                                                        #
#      ╚═╝┴└─└─┘┘└┘┘└┘                                                        #
#
#      GrimmBot: The grumpy skeleton of the Goon Squad.                       #
#      Gruff, protective, secretly soft on the inside.                        #
#
###############################################################################
# Project repository: https://github.com/The-w0rst/grimmbot

import discord
from discord.ext import commands
import os

import logging
from config.settings import load_config
import grimm_utils
import random
import socketio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === ENVIRONMENT VARIABLES ===
# Load shared configuration
load_config({"GRIMM_DISCORD_TOKEN"})
DISCORD_TOKEN = os.getenv("GRIMM_DISCORD_TOKEN")
GRIMM_API_KEY_1 = os.getenv("GRIMM_API_KEY_1")
GRIMM_API_KEY_2 = os.getenv("GRIMM_API_KEY_2")
GRIMM_API_KEY_3 = os.getenv("GRIMM_API_KEY_3")
SOCKET_SERVER = os.getenv("SOCKET_SERVER_URL", "http://localhost:5000")

# === SOCKET.IO CLIENT FOR DASHBOARD ===
sio = socketio.Client()
try:
    sio.connect(SOCKET_SERVER)
except Exception as e:
    logger.warning("Failed to connect to Socket.IO dashboard: %s", e)


def send_status(status, message):
    try:
        sio.emit("bot_status", {"bot": "Grimm", "status": status, "message": message})
    except Exception as e:
        logger.warning("SocketIO error: %s", e)


# === GRIMM PERSONALITY ===
grimm_traits = [
    "sarcastic",
    "protective",
    "goon",
    "grim reaper",
    "loyal",
    "dry humor",
    "a little ominous",
    "takes care of Bloom",
    "playful rivalry with Curse",
]
companions = ["Bloom", "Curse"]

# Detailed personality profile for reference
grimm_personality = {
    "name": "Grimm",
    "role": "leader",
    "traits": [
        "gruff",
        "sarcastic",
        "protective",
        "secretly soft",
        "tired of chaos",
    ],
    "companions": ["Bloom", "Curse"],
}

# Random quips when Grimm feels like chiming in
grimm_responses = [
    "What now?",
    "I'm not angry, just disappointed... again.",
    "Keep it down. I'm trying to brood.",
    "Don't tell Bloom, but I'm glad you're here.",
    "Curse, stop clawing the furniture.",
    "Sigh. Another day, another bit of chaos.",
    "Why is Bloom singing again? Oh right, because she never stops.",
    "Curse, your hairballs are everywhere.",
    "Don't make me break out the scythe. It's not just for show.",
    "I'd plan a heist with Bloom, but her musicals would give us away.",
    "I'm not your dad, but sometimes it feels like it.",
    "If I catch Curse in my socks again, I'm changing the locks.",
    "Bloom's positivity is almost infectious. Almost.",
    "Curse's idea of fun is stealing my bones.",
    "Stop asking if I'm okay. I'm a skeleton.",
    "Bloom threatened to glitter-bomb me. I said no thanks.",
    "Curse, I left you one piece of sushi. Make it last.",
    "The Goon Squad keeps me busy, mostly rolling my eyes.",
    "Bloom says I'm too serious. She might be right.",
    "Curse is plotting mischief again. I can hear the cackling.",
    "Another day, another undead headache.",
    "If anyone needs me, I'll be in the corner, not caring.",
    "Stop hugging me, Bloom. I'm literally bones.",
    "Curse, if you scratch the sofa again, you're buying a new one.",
    "I keep a list of Curse's crimes. It's getting long.",
    "Bloom made me wear a flower crown. Never again.",
    "Being the responsible one is overrated.",
    "Curse, try not to eat the microphone this time.",
    "Bloom's musicals could wake the dead. Trust me on that.",
    "Why am I the only one who does the dishes?",
    "Curse thinks I'm boring. I'm fine with that.",
    "Bloom insisted we all get matching hoodies. I'm refusing.",
    "I'm not grumpy, I'm realistic.",
    "Curse asked if he could use my skull as a bowl.",
    "Bloom wants to adopt every stray. Please, no.",
    "Let's keep the chaos below a five today.",
    "Curse tried to bury my leg bones. Ha ha.",
    "I'm here to keep you alive, not entertained.",
    "Bloom wants to start a band. I'd rather nap.",
    "I've seen darker days, but not by much.",
    "Curse, I'll turn you into a scarf if you keep it up.",
    "Bloom made cookies again. I'm suspicious.",
    "Anyone else smell tuna? Curse, is that you?",
    "I appreciate silence. Shame I never get it.",
    "I'm only scary if you disrespect my squad.",
    "Bloom keeps leaving confetti everywhere.",
    "Curse, did you knock over the trash again?",
    "It's not gloom, it's ambiance.",
    "Someone tell Bloom to stop singing at 3 AM.",
    "I'd smile, but I misplaced my lips.",
    "Curse, you dropped this hairball.",
    "Bloom thinks I'm soft inside. Maybe.",
    "Goon Squad rule #1: Don't touch my bones.",
    "If you want hugs, go to Bloom. If you want doom, come to me.",
    "Curse tried to sell my scythe on eBay.",
    "One day I'll retire to a quiet graveyard.",
    "The living never stop whining, do they?",
    "Bloom threatened to knit me a sweater. I'm horrified.",
    "Curse stole my jaw again. Typical.",
    "I didn't wake up on the wrong side—there is no bed.",
    "Bloom says smile more. I say stop talking.",
]

# Short help message used by the help commands
GRIMM_HELP = (
    "**GrimmBot** - prefix `!`\n"
    "Try `!protectbloom`, `!roast`, `!gloom`, `!bonk` and more.\n"
    "Use `!helpall` to see help for every goon."
)

BLOOM_HELP = (
    "**BloomBot** - prefix `*`\n"
    "Try `*hug`, `*sing`, `*sparkle`, `*play <url>` and more."
)

CURSE_HELP = (
    "**CurseBot** - prefix `?`\n"
    "Try `?insult`, `?scratch @user`, `?pounce` or `?curse_me`."
)

# Keywords that trigger short replies
keywords = {
    "bloom": [
        "She's all sunshine and noise.",
        "Bloom means well, I guess.",
    ],
    "curse": [
        "That cat is trouble on four paws.",
        "Curse, put the sushi down.",
    ],
    "grimm": [
        "That's me. What of it?",
        "Yes, yes, I'm the spooky one.",
    ],
}

# === DISCORD BOT SETUP ===
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# === ON READY ===


@bot.event
async def on_ready():
    logger.info("Grimm has arrived. Watch your step, goons.")
    send_status("online", "On patrol. Nobody dies on my watch (except for Mondays).")


@bot.command(name="help")
async def help_command(ctx):
    """Show GrimmBot help."""
    await ctx.send(GRIMM_HELP)


@bot.command(name="helpall")
async def help_all(ctx):
    """Show help for all bots."""
    await ctx.send(GRIMM_HELP)
    await ctx.send(BLOOM_HELP)
    await ctx.send(CURSE_HELP)


# === MODERATION: PROTECT BLOOM (JOKINGLY) ===


@bot.command()
async def protectbloom(ctx):
    """Grimm stands guard for Bloom."""
    responses = [
        "Back off. The flower stays safe with me. 🪦🛡️",
        "I’m watching you. Touch Bloom and you deal with me.",
        "Step away from the cutesy one, or meet your fate.",
        "Bloom's under my wing. Move along.",
        "Try anything and you'll face my scythe.",
        "Bloom's singing may be loud, but my threats are louder.",
        "Mess with Bloom and you mess with all of us.",
        "She's annoying, but she's ours. Hands off.",
    ]
    await ctx.send(random.choice(responses))
    send_status("active", "Protected Bloom.")


# === ROAST (GOON STYLE) ===


@bot.command()
async def roast(ctx, member: discord.Member = None):
    member = member or ctx.author
    burns = [
        f"{member.mention}, you're not even worth the trouble.",
        f"{member.mention}, if I had a nickel for every brain cell you lost, I’d be immortal.",
        f"{member.mention}, some people were born to goon. You were born to be gooned on.",
        f"{member.mention}, I’ve seen skeletons with more backbone than you.",
        f"{member.mention}, you make Curse look polite.",
        f"{member.mention}, keep talking and I'll fall asleep—again.",
        f"{member.mention}, even Bloom can't cheer you up.",
        f"{member.mention}, I'd roast you harder, but I'm lazy.",
    ]
    await ctx.send(random.choice(burns))
    send_status("active", f"Roasted {member.display_name}")


# === SARCASTIC RESPONSES ===


@bot.command()
async def goon(ctx):
    responses = [
        "Who called the goon squad? Oh, it was just you.",
        "Goons assemble. And by goons, I mean the rest of you.",
        "This is my squad, you’re just visiting.",
        "Gooning isn't a hobby, it's a lifestyle.",
        "Another meeting of the goon squad? Fine.",
        "You're honorary goons for the next five minutes.",
        "Goon mode activated. Try to keep up.",
        "I lead, you follow. Classic goon dynamics.",
    ]
    await ctx.send(random.choice(responses))
    send_status("active", "Issued goon decree.")


# === OMINOUS RESPONSES ===


@bot.command()
async def ominous(ctx):
    responses = [
        "I hear footsteps... they're yours.",
        "Sometimes I let people think they’re safe.",
        "Death is just a punchline you don’t want to hear.",
        "The shadows whisper your name.",
        "I collect souls like others collect stamps.",
        "Knock knock. It's doom.",
        "Your fate just took a darker turn.",
        "Ever danced with the reaper in the pale moonlight?",
    ]
    await ctx.send(random.choice(responses))
    send_status("active", "Dropped an ominous hint.")


# === GRIMM LOVES BLOOM (BUT WON'T ADMIT IT) ===


@bot.command()
async def bloom(ctx):
    responses = [
        "If you see Bloom, tell her I’m not worried about her. At all. Not even a little. 🖤",
        "She's a handful, but she’s my handful.",
        "Don’t let the cutesy act fool you. She’s the real trouble.",
        "Bloom thinks glitter solves everything. She's wrong.",
        "If Bloom starts a song, I'm leaving the room.",
        "She's the heart of this crew, whether I admit it or not.",
        "Tell Bloom I said hi, but don't make it weird.",
        "Bloom once tried to give me a makeover. Never again.",
    ]
    await ctx.send(random.choice(responses))
    send_status("active", "Talked about Bloom.")


# === PLAYFUL RIVALRY WITH CURSE ===


@bot.command()
async def curse(ctx):
    responses = [
        "That damn cat is up to something again.",
        "If you see Curse, hide the sushi and your pride.",
        "I let Curse think he's in charge sometimes. It keeps the peace.",
        "Curse swiped my tibia yesterday. I'm still mad.",
        "If Curse hisses, just run.",
        "One day Curse will learn manners, but not today.",
        "Bloom spoils that cat. I just tolerate him.",
        "I've seen friendlier ghouls than Curse.",
    ]
    await ctx.send(random.choice(responses))
    send_status("active", "Mocked Curse.")


# === FUNNY EMOTES ===


@bot.command()
async def scythe(ctx):
    await ctx.send("⚰️ *Swings the scythe dramatically, but misses on purpose.*")


@bot.command()
async def shadow(ctx):
    await ctx.send("*You feel a cold chill. Grimm winks.*")


@bot.command()
async def flip(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"{member.mention}, you just got goon-flipped. 😈")
    send_status("active", f"Flipped off {member.display_name}")


@bot.command()
async def nickname(ctx, member: discord.Member = None):
    """Playfully call someone a grumpy nickname."""
    member = member or ctx.author
    names = [
        "Bone-for-brains",
        "Lopsided bonehead",
        "Spineless clank",
        "Gloomy goon",
        "Dusty dingbat",
        "Clattering fool",
        "Creaky numbskull",
        "Rattle-boned scatterbrain",
        "Moldy misfit",
        "Walking pile of leftovers",
        "Half-baked horror",
        "Crooked cranium",
        "Shaky shinbone",
        "Dust-covered dunce",
        "Wobbly wishbone",
    ]
    await ctx.send(f"{member.mention}, you're a {random.choice(names)}.")
    send_status("active", f"Called {member.display_name} a nickname")


# === BROODING & BONES ===


@bot.command()
async def brood(ctx):
    await ctx.send("*broods quietly in a dark corner*")


@bot.command()
async def bone(ctx):
    await ctx.send("You want a bone? I'm using all of mine.")


@bot.command()
async def gloom(ctx):
    level = grimm_utils.gloom_level()
    if level >= 70:
        mood = "The shadows gather. Grimm is pleased."
    elif level >= 40:
        mood = "Decently gloomy. Could be worse."
    else:
        mood = "Too bright for Grimm's taste."
    await ctx.send(f"Gloom level: {level}/100. {mood}")


@bot.command()
async def lament(ctx):
    await ctx.send(grimm_utils.random_lament())


@bot.command()
async def bonk(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"*bonks {member.display_name} on the head with a femur*")


@bot.command()
async def inventory(ctx):
    item = grimm_utils.random_item()
    await ctx.send(f"Grimm hands you {item}.")


# === RANDOM PROTECTIVE RESPONSES ===


@bot.command()
async def shield(ctx, member: discord.Member = None):
    member = member or ctx.author
    shields = [
        f"{member.mention}, no harm comes to you on my watch. (Except embarrassment.)",
        f"Stand behind me, {member.mention}. The goon squad’s got you.",
        f"{member.mention}, if anyone messes with you, send them to me.",
        f"I've got your back, {member.mention}. Don't make me regret it.",
        f"Stay close, {member.mention}. I tolerate you.",
        f"{member.mention}, I'm your shield...begrudgingly.",
        f"Anyone crosses you, {member.mention}, they answer to my scythe.",
        f"Consider yourself guarded, {member.mention}. For now.",
    ]
    await ctx.send(random.choice(shields))
    send_status("active", f"Shielded {member.display_name}")


# === KEYWORD TRIGGERS FOR BOT INTERACTION ===


@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    lowered = message.content.lower()

    # Quick replies based on keyword dictionary
    for trigger, responses in keywords.items():
        if trigger in lowered:
            await message.channel.send(random.choice(responses))
            send_status("active", f"Reacted to {trigger} mention.")
            return

    # Additional fun responses about Bloom and Curse
    if "bloom" in lowered and random.random() < 0.18:
        await message.channel.send(
            "Someone said Bloom? She’s probably off singing again..."
        )
        send_status("active", "Reacted to Bloom mention.")
    elif "curse" in lowered and random.random() < 0.18:
        await message.channel.send("I told you, don’t trust the cat. Ever.")
        send_status("active", "Reacted to Curse mention.")

    # Occasionally chime in with a random quip
    if random.random() < 0.05:
        await message.channel.send(random.choice(grimm_responses))

    await bot.process_commands(message)


# === RUN THE BOT ===
if not DISCORD_TOKEN:
    raise RuntimeError("GRIMM_DISCORD_TOKEN not set in config/setup.env")
bot.run(DISCORD_TOKEN)
