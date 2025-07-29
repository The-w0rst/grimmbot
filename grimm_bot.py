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
import asyncio
import openai
import datetime

import logging
from config.settings import load_config
import grimm_utils
import random
import socketio
from src.logger import setup_logging, log_message

# Configure logging
setup_logging("grimm_bot.log")
logger = logging.getLogger(__name__)

# === ENVIRONMENT VARIABLES ===
# Load shared configuration
load_config({"GRIMM_DISCORD_TOKEN"})
DISCORD_TOKEN = os.getenv("GRIMM_DISCORD_TOKEN")
GRIMM_API_KEY_1 = os.getenv("GRIMM_API_KEY_1")
GRIMM_API_KEY_2 = os.getenv("GRIMM_API_KEY_2")
GRIMM_API_KEY_3 = os.getenv("GRIMM_API_KEY_3")
GRIMM_OPENAI_KEY = os.getenv("GRIMM_OPENAI_KEY")
GRIMM_GPT_ENABLED = os.getenv("GRIMM_GPT_ENABLED", "true").lower() == "true"
GRIMM_OPENAI_MODEL = os.getenv("GRIMM_OPENAI_MODEL", "gpt-3.5-turbo")
SOCKET_SERVER = os.getenv("SOCKET_SERVER_URL", "http://localhost:5000")


def check_required() -> None:
    missing = []
    for var in ("GRIMM_DISCORD_TOKEN", "GRIMM_OPENAI_KEY"):
        val = os.getenv(var)
        if not val:
            missing.append(var)
    if missing:
        logger.error("Missing required variables: %s", ", ".join(missing))
        raise SystemExit(1)


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
START_TIME = datetime.datetime.utcnow()

# === ON READY ===


@bot.event
async def on_ready():
    check_required()
    guilds = ", ".join(g.name for g in bot.guilds)
    cogs = ", ".join(bot.cogs.keys())
    env_summary = {
        "GRIMM_DISCORD_TOKEN": (DISCORD_TOKEN[:4] + "...") if DISCORD_TOKEN else "missing",
        "GRIMM_OPENAI_KEY": (GRIMM_OPENAI_KEY[:4] + "...") if GRIMM_OPENAI_KEY else "missing",
    }
    logger.info("Grimm online | guilds: %s | cogs: %s | env: %s", guilds, cogs, env_summary)
    log_message("Grimm bot ready")
    send_status("online", "On patrol. Nobody dies on my watch (except for Mondays).")


@bot.event
async def on_command_error(ctx, error):
    """Handle command errors with a friendly message."""
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Slow down! Try again in {round(error.retry_after, 1)}s.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You lack the permissions for that command.")
    else:
        await ctx.send("An error occurred. Check logs for details.")
    logger.error("Command error: %s", error)


# === ChatGPT Integration ===
async def chatgpt_reply(prompt: str) -> str:
    """Return a response from OpenAI in Grimm's voice.

    Update ``GRIMM_OPENAI_MODEL`` in the environment or the ``model``
    argument below to switch models (e.g. ``gpt-4o``).
    """
    if not GRIMM_GPT_ENABLED:
        return "ChatGPT features are disabled."
    if not GRIMM_OPENAI_KEY:
        return "OpenAI key missing for Grimm."
    client = openai.AsyncOpenAI(api_key=GRIMM_OPENAI_KEY)
    try:
        response = await client.chat.completions.create(
            model=GRIMM_OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Grimm, a grumpy but protective skeleton. "
                        "Keep replies short and sarcastic."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.8,
        )
        logger.info("OpenAI usage: %s tokens", response.usage.total_tokens)
        return response.choices[0].message.content.strip()
    except openai.RateLimitError:
        return "OpenAI rate limit hit. Try again later."
    except Exception as exc:  # Catch APIError and others
        logger.error("OpenAI error: %s", exc)
        return "Problem contacting OpenAI."


async def _collect_statement(member: discord.Member, issue: str) -> str | None:
    """DM ``member`` for their side of the issue."""
    try:
        await member.send(f"What's your side on '{issue}'?")
    except discord.Forbidden:
        return None

    def check(m: discord.Message) -> bool:
        return m.author == member and isinstance(m.channel, discord.DMChannel)

    try:
        msg = await bot.wait_for("message", check=check, timeout=120)
    except asyncio.TimeoutError:
        return None
    return msg.content.strip()


@bot.event
async def on_guild_join(guild):
    logger.info("Joined guild: %s", guild.name)


@bot.event
async def on_guild_remove(guild):
    logger.info("Removed from guild: %s", guild.name)


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


@bot.command(name="ask")
async def ask(ctx, *, question: str):
    """Ask Grimm a question via ChatGPT."""
    reply = await chatgpt_reply(question)
    for chunk in [reply[i : i + 1900] for i in range(0, len(reply), 1900)]:
        await ctx.send(chunk)


@bot.command(name="health")
async def health(ctx):
    """Report bot health statistics."""
    try:
        uptime = datetime.datetime.utcnow() - START_TIME
        latency = round(bot.latency * 1000)
        api_status = "ok" if GRIMM_OPENAI_KEY else "no key"
        msg = (
            f"Uptime: {uptime}\n"
            f"Ping: {latency} ms\n"
            f"Cogs: {len(bot.cogs)} loaded\n"
            f"OpenAI: {api_status}"
        )
        await ctx.send(msg)
    except Exception as exc:
        logger.exception("health command failed: %s", exc)


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


@bot.command(name="judge")
@commands.cooldown(1, 60, commands.BucketType.user)
async def judge(ctx, other: discord.Member, *, issue: str):
    """Let Grimm judge an argument. Users DM their sides."""
    side1 = await _collect_statement(ctx.author, issue)
    if side1 is None:
        await ctx.send(f"Couldn't get {ctx.author.display_name}'s statement.")
        return
    side2 = await _collect_statement(other, issue)
    if side2 is None:
        await ctx.send(f"Couldn't get {other.display_name}'s statement.")
        return
    prompt = (
        f"Issue: {issue}\n"
        f"User1 ({ctx.author.display_name}): {side1}\n"
        f"User2 ({other.display_name}): {side2}\n"
        "Give your verdict in character as Grimm."
    )
    reply = await chatgpt_reply(prompt)
    for chunk in [reply[i : i + 1900] for i in range(0, len(reply), 1900)]:
        await ctx.send(chunk)


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
check_required()

try:
    bot.run(DISCORD_TOKEN)
finally:
    log_message("Grimm shutting down")
