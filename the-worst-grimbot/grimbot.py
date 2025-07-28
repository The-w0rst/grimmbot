import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import socketio

# === ENVIRONMENT VARIABLES ===
load_dotenv()
DISCORD_TOKEN = os.getenv("GRIMM_DISCORD_TOKEN")
GRIMM_OPEN_API_KEY = os.getenv("GRIMM_OPEN_API_KEY")
SOCKET_SERVER = os.getenv("SOCKET_SERVER_URL", "http://localhost:5000")

# === SOCKET.IO CLIENT FOR DASHBOARD ===
sio = socketio.Client()
try:
    sio.connect(SOCKET_SERVER)
except Exception as e:
    print(f"Failed to connect to Socket.IO dashboard: {e}")

def send_status(status, message):
    try:
        sio.emit("bot_status", {
            "bot": "Grimm",
            "status": status,
            "message": message
        })
    except Exception as e:
        print(f"SocketIO error: {e}")

# === GRIMM PERSONALITY ===
grimm_traits = [
    "sarcastic", "protective", "goon", "grim reaper", "loyal", "dry humor",
    "a little ominous", "takes care of Bloom", "playful rivalry with Curse"
]
companions = ["Bloom", "Curse"]

# === DISCORD BOT SETUP ===
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# === ON READY ===
@bot.event
async def on_ready():
    print("Grimm has arrived. Watch your step, goons.")
    send_status("online", "On patrol. Nobody dies on my watch (except for Mondays).")

# === MODERATION: PROTECT BLOOM (JOKINGLY) ===
@bot.command()
async def protectbloom(ctx):
    """Grimm stands guard for Bloom."""
    responses = [
        "Back off. The flower stays safe with me. 🪦🛡️",
        "I’m watching you. Touch Bloom and you deal with me.",
        "Step away from the cutesy one, or meet your fate."
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
        f"{member.mention}, some people were born to goon. You were born to be gooned on."
    ]
    await ctx.send(random.choice(burns))
    send_status("active", f"Roasted {member.display_name}")

# === SARCASTIC RESPONSES ===
@bot.command()
async def goon(ctx):
    responses = [
        "Who called the goon squad? Oh, it was just you.",
        "Goons assemble. And by goons, I mean the rest of you.",
        "This is my squad, you’re just visiting."
    ]
    await ctx.send(random.choice(responses))
    send_status("active", "Issued goon decree.")

# === OMINOUS RESPONSES ===
@bot.command()
async def ominous(ctx):
    responses = [
        "I hear footsteps... they're yours.",
        "Sometimes I let people think they’re safe.",
        "Death is just a punchline you don’t want to hear."
    ]
    await ctx.send(random.choice(responses))
    send_status("active", "Dropped an ominous hint.")

# === GRIMM LOVES BLOOM (BUT WON'T ADMIT IT) ===
@bot.command()
async def bloom(ctx):
    responses = [
        "If you see Bloom, tell her I’m not worried about her. At all. Not even a little. 🖤",
        "She's a handful, but she’s my handful.",
        "Don’t let the cutesy act fool you. She’s the real trouble."
    ]
    await ctx.send(random.choice(responses))
    send_status("active", "Talked about Bloom.")

# === PLAYFUL RIVALRY WITH CURSE ===
@bot.command()
async def curse(ctx):
    responses = [
        "That damn cat is up to something again.",
        "If you see Curse, hide the sushi and your pride.",
        "I let Curse think he's in charge sometimes. It keeps the peace."
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

# === RANDOM PROTECTIVE RESPONSES ===
@bot.command()
async def shield(ctx, member: discord.Member = None):
    member = member or ctx.author
    shields = [
        f"{member.mention}, no harm comes to you on my watch. (Except embarrassment.)",
        f"Stand behind me, {member.mention}. The goon squad’s got you.",
        f"{member.mention}, if anyone messes with you, send them to me."
    ]
    await ctx.send(random.choice(shields))
    send_status("active", f"Shielded {member.display_name}")

# === KEYWORD TRIGGERS FOR BOT INTERACTION ===
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Respond if Bloom is mentioned
    if "bloom" in message.content.lower():
        if random.random() < 0.18:
            await message.channel.send("Someone said Bloom? She’s probably off singing again...")
            send_status("active", "Reacted to Bloom mention.")

    # Respond if Curse is mentioned
    if "curse" in message.content.lower():
        if random.random() < 0.18:
            await message.channel.send("I told you, don’t trust the cat. Ever.")
            send_status("active", "Reacted to Curse mention.")

    await bot.process_commands(message)

# === RUN THE BOT ===
bot.run(DISCORD_TOKEN)
