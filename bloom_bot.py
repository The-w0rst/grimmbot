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
# Project repository: https://github.com/The-w0rst/grimmbot

import discord
from discord.ext import commands
import random
import os
import asyncio
import openai
import logging
from config.settings import load_config
from pathlib import Path
import yt_dlp
from src.logger import setup_logging, log_message

# Configure logging
setup_logging("bloom_bot.log")
logger = logging.getLogger(__name__)

# Load a single shared configuration file for all bots
ENV_PATH = Path(__file__).resolve().parent / "config" / "setup.env"
if not ENV_PATH.exists():
    raise SystemExit("config/setup.env missing. Run 'python install.py' first.")
load_config({"BLOOM_DISCORD_TOKEN"})
DISCORD_TOKEN = os.getenv("BLOOM_DISCORD_TOKEN")
BLOOM_API_KEY_1 = os.getenv("BLOOM_API_KEY_1")
BLOOM_API_KEY_2 = os.getenv("BLOOM_API_KEY_2")
BLOOM_API_KEY_3 = os.getenv("BLOOM_API_KEY_3")
BLOOM_OPENAI_KEY = os.getenv("BLOOM_OPENAI_KEY")
BLOOM_GPT_ENABLED = os.getenv("BLOOM_GPT_ENABLED", "true").lower() == "true"
BLOOM_OPENAI_MODEL = os.getenv("BLOOM_OPENAI_MODEL", "gpt-3.5-turbo")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="*", intents=intents, help_command=None)

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
        "loves silly jokes",
    ],
    "companions": ["Grimm", "Curse"],
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
    "Who needs sleep when we have each other?",
    "Let's paint the town pastel!",
    "I'm mailing you a virtual hug right now!",
    "Any excuse for a dance break, right?",
    "Glitter makes everything better, trust me!",
    "Let's turn this chat into a mini musical!",
    "Musicals at midnight? Count me in!",
    "Glitter here, glitter there, glitter everywhere!",
    "Who wants to join my spontaneous karaoke?",
    "I just hugged a pillow thinking it was you!",
    "Boba first, questions later!",
]

# Short help message used by the help commands
BLOOM_HELP = (
    "**BloomBot** - prefix `*`\n"
    "Try `*hug`, `*sing`, `*sparkle`, `*play <url>` and more.\n"
    "Use `*helpall` to see help for every goon."
)

GRIMM_HELP = (
    "**GrimmBot** - prefix `!`\n"
    "Try `!protectbloom`, `!roast`, `!gloom`, `!bonk` and more."
)

CURSE_HELP = (
    "**CurseBot** - prefix `?`\n"
    "Try `?insult`, `?scratch @user`, `?pounce` or `?curse_me`."
)

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
    "Boys, let's conquer the day with joy!",
    "Boy, you're rocking those vibes!",
    "Boys, more jokes, less worries!",
    "Boy oh boy, let's level up the fun!",
    "Boys, let's spam Grimm with selfies!",
    "Boy, keep shining like the star you are!",
]

# === Bloom Queen Lines ===
queen_lines = [
    "Yas queen! Slay the day!",
    "Queens, keep those crowns high!",
    "Hey girl, you're unstoppable!",
    "Yas queen, your sparkle is unmatched!",
    "Girls just wanna have fun and rule!",
    "Queen vibes only, let's shine!",
    "You go girl, absolutely iconic!",
    "Yaaaas queen, keep shining bright!",
    "Girls, let's conquer with kindness!",
    "Queen energy incoming! 💖",
    "Slay it, queen! You got this!",
    "Hey queen, want some boba?",
    "Queens unite for a dance party!",
    "Yas, girls! Let's make magic happen!",
    "Queen, your confidence is contagious!",
    "Girls, keep being amazing!",
    "Yas queen, the world is yours!",
    "Queen power! Nothing can stop us!",
    "Hey queens, time to sparkle!",
    "Girls rule, everyone else drools!",
    "Yas queen, show off that style!",
    "Queen squad, assemble!",
    "Keep that crown polished, girl!",
    "Queens, let's turn up the glitter!",
    "You're royalty, girl—don't forget it!",
    "Yas queen, strut your stuff!",
    "Queens, bring on the sparkle storm!",
    "Hey girl, your crown looks amazing today!",
    "Queens rise above the drama!",
    "Yas queen, keep slaying with kindness!",
]

# === EPIC: The Musical Track List ===
# Organized by saga name with every released song.
epic_songs = {
    "The Troy Saga": [
        "The Horse and the Infant",
        "Just a Man",
        "Full Speed Ahead",
        "Open Arms",
        "Warrior of the Mind",
    ],
    "The Cyclops Saga": [
        "Polyphemus",
        "Survive",
        "Remember Them",
        "My Goodbye",
    ],
    "The Ocean Saga": [
        "Storm",
        "Luck Runs Out",
        "Keep Your Friends Close",
        "Ruthlessness",
    ],
    "The Circe Saga": [
        "Puppeteer",
        "Wouldn’t You Like",
        "Done For",
        "There Are Other Ways",
    ],
    "The Underworld Saga": [
        "The Underworld",
        "No Longer You",
        "Monster",
    ],
    "The Thunder Saga": [
        "Suffering",
        "Different Beast",
        "Scylla",
        "Mutiny",
        "Thunder Bringer",
    ],
    "The Wisdom Saga": [
        "Legendary",
        "Little Wolf",
        "We’ll Be Fine",
        "Love in Paradise",
        "God Games",
    ],
    "The Vengeance Saga": [
        "Not Sorry for Loving You",
        "Dangerous",
        "Charybdis",
        "Get in the Water",
        "Six Hundred Strike",
    ],
    "The Ithaca Saga": [
        "The Challenge",
        "Hold Them Down",
        "Odysseus",
        "I Can’t Help but Wonder",
        "Would You Fall in Love with Me Again",
    ],
}

# Optional lyrics for EPIC songs. This dictionary can be filled with full
# lyrics if you have permission to use them. Each song maps to a list of
# lines that can be sung.  By default it is left empty so you can provide
# your own files in ``localtracks/epic_lyrics``.
epic_lyrics: dict[str, list[str]] = {}

# Directory containing optional lyric text files.  Each file should be named
# after the song, lowercase with spaces replaced by underscores and a
# ``.txt`` extension, e.g. ``the_horse_and_the_infant.txt``.  Lines in the
# file are sent one by one when singing.
EPIC_LYRICS_DIR = Path(__file__).resolve().parent / "localtracks" / "epic_lyrics"
EPIC_LYRICS_DIR.mkdir(parents=True, exist_ok=True)


def load_epic_lyrics(song: str) -> list[str]:
    """Return lyric lines for ``song`` loaded from ``EPIC_LYRICS_DIR``."""
    slug = (
        song.lower()
        .replace("'", "")
        .replace("’", "")
        .replace(" ", "_")
    )
    path = EPIC_LYRICS_DIR / f"{slug}.txt"
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


async def perform_drama(
    bot: commands.Bot, ctx: commands.Context, song: str | None = None
):
    """Interactive EPIC sing-along helper."""
    all_songs = [s for songs in epic_songs.values() for s in songs]

    if song and song.lower() == "list":
        msg_lines = ["**Available EPIC songs:**"]
        for saga, songs in epic_songs.items():
            msg_lines.append(f"__{saga}__")
            msg_lines.extend(f"- {title}" for title in songs)
        await ctx.send("\n".join(msg_lines))
        return

    chosen = None
    if song:
        for s in all_songs:
            if s.lower() == song.lower():
                chosen = s
                break
        if not chosen:
            await ctx.send("Song not found. Use `*drama list` to see options.")
            return
    else:
        chosen = random.choice(all_songs)

    await ctx.send(f"🎭 **EPIC: The Musical** – let's sing **{chosen}**!")

    lyrics = epic_lyrics.get(chosen) or load_epic_lyrics(chosen)
    if not lyrics:
        await ctx.send(
            "(Lyrics missing – add them in `localtracks/epic_lyrics` to sing along!)"
        )
        return

    await ctx.send("Type `full` for the entire song or `snippet` for a short excerpt.")

    def check(m: discord.Message) -> bool:
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        reply = await bot.wait_for("message", timeout=15, check=check)
        choice = reply.content.lower().strip()
    except asyncio.TimeoutError:
        choice = "snippet"

    if choice.startswith("full"):
        lines_to_send = lyrics
    else:
        count = max(1, min(len(lyrics), random.randint(4, 8)))
        start = random.randint(0, max(0, len(lyrics) - count))
        lines_to_send = lyrics[start : start + count]

    for line in lines_to_send:
        await ctx.send(line)
        await asyncio.sleep(1)


# Lines from Bloom's favorite song "Pretty Little Baby" by Connie Francis
pretty_little_baby_lines = [
    "Pretty little baby (ya-ya)",
    "You say that maybe you'll be thinkin' of me",
    "And tryin' to love me",
    "Pretty little baby, I'm hoping that you do",
    "Ask your mama, your papa, your sister or your brother",
    "If they've ever loved another like I love you",
    "Come closer, pretty baby, and whisper softly",
    "Hold me tight and never let me go",
    "Pretty little baby, let your love light shine",
    "Don't you know I'm waiting just for you",
    "Pretty little baby, I'll always be true",
]

comfort_lines = [
    "Deep breaths, you've totally got this!",
    "Bloom believes in you more than bubble tea!",
    "Sending cuddles and sunshine your way!",
    "You're stronger than you know, friend!",
    "I'll stand by you with glittery support!",
]

story_lines = [
    "Once upon a sparkle, you saved the day!",
    "In a world of boba, you were the hero we needed.",
    "There was a cat, a skeleton, and you—chaos ensued!",
    "Legend tells of your epic dance moves across the land.",
    "Every good story starts with a hug from Bloom!",
]

goodnight_lines = [
    "Nighty night! Dream of bubble tea rivers!",
    "May your dreams be filled with musicals and friends!",
    "Sleep tight and don't let the glitter bite!",
    "Rest well, tomorrow we'll cause more chaos!",
    "Goodnight superstar, you deserve a break!",
]

# === Keyword Triggers ===
keywords = {
    "grimm": ["Grimm is my spooky bestie.", "He acts tough, but he's a sweetheart."],
    "curse": [
        "Curse is such a gremlin cat. I love him!",
        "He tried to eat my controller again...",
    ],
    "hug": ["HUG TIME! Ready or not! 🥢", "*wraps you in love and chaos*"],
    "sing": pretty_little_baby_lines,
    "boba": ["Bubble tea buddies unite!", "I could drink boba all day!"],
    "compliment": [
        "You're shining brighter than my glitter!",
        "Compliments inbound: you're amazing!",
    ],
    "comfort": comfort_lines,
    "story": story_lines,
    "goodnight": goodnight_lines,
    "gn": goodnight_lines,
    "queen": queen_lines,
    "girl": queen_lines,
    "girls": queen_lines,
    "boy": boy_lines,
    "boys": boy_lines,
    "squad": ["GOON SQUAD roll call: Grimm 💀, Bloom 🌸, Curse 🐾. Chaos and comfort!"],
}

# === Inter-Bot Interactions ===
interactions = [
    "Bloom: Grimm, you’re not as scary as you look!",
    "Bloom: Curse, put down the sushi and join the dance!",
    "Grimm: Bloom, can you stop with the glitter? No? Okay...",
    "Curse: Hiss. (But like, the friendly kind. Maybe.)",
    "Bloom: Goon Squad! Assemble for hugs!",
    "Grimm: Bloom, no more musicals during meetings.",
    "Curse: I'll trade you sushi for silence, Bloom.",
    "Bloom: Curse, quit shedding on my costumes!",
    "Grimm: Both of you, behave for five minutes.",
    "Curse: Only if Bloom stops singing.",
]


# === ChatGPT Integration ===
async def chatgpt_reply(prompt: str) -> str:
    """Return a response from OpenAI in Bloom's bubbly voice.

    Change ``BLOOM_OPENAI_MODEL`` in the environment or below to use
    a different model such as ``gpt-4o``.
    """
    if not BLOOM_GPT_ENABLED:
        return "ChatGPT features are disabled."
    if not BLOOM_OPENAI_KEY:
        return "OpenAI key missing for Bloom."
    client = openai.AsyncOpenAI(api_key=BLOOM_OPENAI_KEY)
    try:
        response = await client.chat.completions.create(
            model=BLOOM_OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Bloom, an energetic reaper who loves musicals,"
                        " hugs and glitter. Respond with enthusiasm and emojis."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.9,
        )
        logger.info("OpenAI usage: %s tokens", response.usage.total_tokens)
        return response.choices[0].message.content.strip()
    except openai.RateLimitError:
        return "OpenAI rate limit hit. Try again later."
    except Exception as exc:
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

# === On Ready ===


@bot.event
async def on_ready():
    logger.info("%s is online and ready to hug the whole server!", bloom_personality["name"])
    log_message("Bloom bot ready")


@bot.command(name="help")
async def help_command(ctx):
    """Show BloomBot help."""
    await ctx.send(BLOOM_HELP)


@bot.command(name="helpall")
async def help_all(ctx):
    """Show help for all bots."""
    await ctx.send(GRIMM_HELP)
    await ctx.send(BLOOM_HELP)
    await ctx.send(CURSE_HELP)


@bot.command(name="ask")
async def ask(ctx, *, question: str):
    """Ask Bloom a question via ChatGPT."""
    reply = await chatgpt_reply(question)
    for chunk in [reply[i : i + 1900] for i in range(0, len(reply), 1900)]:
        await ctx.send(chunk)


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
    await ctx.send(random.choice(pretty_little_baby_lines) + " 🎶")


@bot.command()
async def karaoke(ctx, *, song: str | None = None):
    """Start a mini karaoke moment."""
    lines = pretty_little_baby_lines
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
        "Believe in yourself, or I’ll believe for you!",
        "You've got this, superstar!",
        "Every step you take is awesome!",
        "Smile big, you're amazing!",
        "Cheering for you from the digital sidelines!",
        "You're a goon squad legend in the making!",
    ]
    await ctx.send(random.choice(cheers))


@bot.command()
async def sparkle(ctx):
    await ctx.send("*throws confetti and joy everywhere* ✨")
    if random.random() < 0.25:
        compliment = random.choice(
            [
                "You're shining brighter than my glitter!",
                "Glitter looks good on you!",
                "You're absolutely dazzling!",
                "Bloom thinks you're fabulous!",
            ]
        )
        await ctx.send(f"{ctx.author.mention} gets covered in glitter! {compliment}")


@bot.command()
async def drama(ctx, *, song: str | None = None):
    """Interactive EPIC song performance."""
    await perform_drama(bot, ctx, song)


@bot.command()
async def play(ctx, url: str):
    """Stream audio from a YouTube URL into your voice channel."""
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("Join a voice channel first.")
        return
    voice = ctx.voice_client
    if voice is None:
        voice = await ctx.author.voice.channel.connect()
    elif voice.channel != ctx.author.voice.channel:
        await voice.move_to(ctx.author.voice.channel)
    ydl_opts = {"format": "bestaudio", "quiet": True}

    def _extract() -> dict:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    info = await asyncio.to_thread(_extract)
    audio_url = info["url"]
    source = await discord.FFmpegOpusAudio.from_probe(audio_url)
    voice.play(source)
    await ctx.send(f"Now playing: {info.get('title', 'unknown')}")


@bot.command()
async def stop(ctx):
    """Stop playback and disconnect."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected.")


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
        "You're sweeter than all the bubble tea!",
        "Your positivity is contagious!",
        "You glow brighter than neon lights!",
        "Your creativity inspires me!",
        "You're the heart of this squad!",
    ]
    await ctx.send(random.choice(compliments))


@bot.command()
async def boy(ctx):
    """Share a playful boy-themed line."""
    await ctx.send(random.choice(boy_lines))


@bot.command()
async def queen(ctx):
    """Share a playful yas queen-style line."""
    await ctx.send(random.choice(queen_lines))


@bot.command()
async def dance(ctx):
    """Start a random dance party."""
    moves = ["Cha-cha-cha!", "Time to boogie!", "Let's breakdance!"]
    await ctx.send(random.choice(moves) + " 💃")


@bot.command()
async def sunshine(ctx):
    """Shower the chat with sunshine."""
    quotes = [
        "Sunshine, lollipops, and rainbows!",
        "You're my little ray of light!",
        "Let's chase the clouds away!",
    ]
    await ctx.send(random.choice(quotes))


@bot.command()
async def flower(ctx):
    """Share a virtual flower."""
    flowers = ["🌸", "🌺", "🌷", "🌻", "💮"]
    await ctx.send(random.choice(flowers) + " for you!")


@bot.command()
async def comfort(ctx):
    """Offer supportive words."""
    await ctx.send(random.choice(comfort_lines))


@bot.command()
async def story(ctx):
    """Tell a short whimsical story."""
    await ctx.send(random.choice(story_lines))


@bot.command(name="judge")
@commands.cooldown(1, 60, commands.BucketType.user)
async def judge(ctx, other: discord.Member, *, issue: str):
    """Ask Bloom to judge an argument between you and someone else."""
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
        "Give your verdict in character as Bloom."
    )
    reply = await chatgpt_reply(prompt)
    for chunk in [reply[i : i + 1900] for i in range(0, len(reply), 1900)]:
        await ctx.send(chunk)


@bot.command()
async def goodnight(ctx):
    """Say goodnight with flair."""
    await ctx.send(random.choice(goodnight_lines))


if not DISCORD_TOKEN:
    raise RuntimeError("BLOOM_DISCORD_TOKEN not set in config/setup.env")
asyncio.run(bot.load_extension("cogs.bloom_cog"))
try:
    bot.run(DISCORD_TOKEN)
finally:
    log_message("Bloom shutting down")
