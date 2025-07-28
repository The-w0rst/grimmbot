import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import openai
import socketio
import random

# === ENVIRONMENT VARIABLES ===
load_dotenv()
DISCORD_TOKEN = os.getenv("BLOOM_DISCORD_TOKEN")
BLOOM_OPEN_API_KEY = os.getenv("BLOOM_OPEN_API_KEY")
SOCKET_SERVER = os.getenv("SOCKET_SERVER_URL", "http://localhost:5000")

openai.api_key = BLOOM_OPEN_API_KEY

# === SOCKET.IO CLIENT FOR DASHBOARD ===
sio = socketio.Client()
try:
    sio.connect(SOCKET_SERVER)
except Exception as e:
    print(f"Failed to connect to Socket.IO dashboard: {e}")


def send_status(status, message):
    try:
        sio.emit("bot_status", {
            "bot": "Bloom",
            "status": status,
            "message": message
        })
    except Exception as e:
        print(f"SocketIO error: {e}")


# === BLOOM PERSONALITY ===
bloom_traits = [
    "goofy", "funny", "cutesy", "playful", "energetic", "loving",
    "sings a lot", "plays video games", "loves theater", "takes care of others",
    "orange cloak", "flower in hair"
]
companions = ["Grimm", "Curse"]

# === DISCORD BOT SETUP ===
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="*", intents=intents)

# === ON READY ===


@bot.event
async def on_ready():
    print("Bloom has entered the server and is ready to brighten your day! 🌼")
    send_status("online", "Blooming and ready to hug everyone!")

# === BLOOM CHAT (OpenAI Integration) ===


@bot.command()
async def chat(ctx, *, prompt: str):
    """Chat with Bloom!"""
    send_status("active", f"Chatted with {ctx.author.display_name}")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if available
            messages=[
                {"role": "system", "content":
                    "You are Bloom, a playful, energetic, loving, and cutesy female reaper. "
                    "You love singing, video games, theater, hugs, and helping others. "
                    "Stay in character, use lots of positive energy and emojis, and be a supportive friend. "
                    "You wear an orange cloak and a flower in your hair. You adore Grimm (your best friend) and Curse (the mischievous cat)."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.88,
        )
        reply = response.choices[0].message.content.strip()
        await ctx.send(reply)
    except Exception:
        await ctx.send("Oops! My flower got tangled. I can't chat right now.")

# === CUTESY, PLAYFUL, FUN COMMANDS ===


@bot.command()
async def hug(ctx, member: discord.Member = None):
    """Send a Bloom hug!"""
    member = member or ctx.author
    hugs = [
        f"{member.mention}, you just got the biggest, fluffiest hug from Bloom! 🧡",
        f"Bloom wraps {member.mention} in a warm orange cloak hug! 🌼",
        f"{member.mention}, consider yourself hugged... and maybe sung to, too! 🎵🧡"
    ]
    await ctx.send(random.choice(hugs))
    send_status("active", f"Hugged {member.display_name}")


@bot.command()
async def sing(ctx):
    """Bloom sings for you!"""
    tunes = [
        "🎤 La la la! You got a special Bloom serenade! 🌷",
        "🎶 Bloom is singing your favorite tune... probably off-key, but with love!",
        "🌼 Do re mi fa so la ti da! (Bloom twirls in her cloak)"
    ]
    await ctx.send(random.choice(tunes))
    send_status("active", "Sang a song!")


@bot.command()
async def energy(ctx):
    """Bloom boosts your energy!"""
    boosts = [
        "💥 ENERGY BLAST! Now go do something amazing!",
        "🌟 ZOOM! You’re now powered by Bloom for the next 24 hours.",
        "🍊 Vitamin C from my cloak! Energized!"
    ]
    await ctx.send(random.choice(boosts))
    send_status("active", "Gave an energy boost!")


@bot.command()
async def compliment(ctx, member: discord.Member = None):
    """Bloom gives a compliment!"""
    member = member or ctx.author
    compliments = [
        f"{member.mention}, your vibes are the best on this server! 🌞",
        f"{member.mention}, Bloom thinks you have a wonderful soul! 🧡",
        f"{member.mention}, if hugs were currency, you’d be a millionaire! 💰🌷"
    ]
    await ctx.send(random.choice(compliments))
    send_status("active", f"Gave a compliment to {member.display_name}")

# === FUN EMOTES ===


@bot.command()
async def flower(ctx):
    """Bloom drops a flower!"""
    await ctx.send("🌸🌼🌸 *Bloom drops a handful of magical flowers!*")


@bot.command()
async def lovegrimm(ctx):
    await ctx.send("Grimm is the best! 🖤🌼 (Don’t tell him I said that...)")
    send_status("active", "Mentioned Grimm lovingly.")


@bot.command()
async def annoycurse(ctx):
    await ctx.send("Hey Curse, catch! *throws a fake sushi* 🐟 (He’s gonna be so mad)")
    send_status("active", "Annoyed Curse.")

# === KEYWORD INTERACTIONS WITH OTHER BOTS ===


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Shoutout if Grimm is mentioned
    if "grimm" in message.content.lower():
        if random.random() < 0.2:
            await message.channel.send("He’s SOOOO grumpy sometimes, but he’s my favorite goon. 🖤")
            send_status("active", "Talked about Grimm.")

    # Tease Curse if mentioned
    if "curse" in message.content.lower():
        if random.random() < 0.2:
            await message.channel.send("Did someone say cursed cat? Where is that little gremlin? 🐾")
            send_status("active", "Talked about Curse.")

    await bot.process_commands(message)

# === RUN THE BOT ===
bot.run(DISCORD_TOKEN)
