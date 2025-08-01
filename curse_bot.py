################################################################################
#                                                                              #
#      ╔═╗╦ ╦╔═╗╦═╗╔═╗                                                        #
#      ║ ╦║ ║╠═╣╠╦╝║╣                                                         #
#      ╚═╝╚═╝╩ ╩╩╚═╚═╝                                                        #
#                                                                              #
#      CurseBot: The mischievous calico chaos.                                #
#      Snarky. Indifferent. Fond of sushi. Hates being cute.                  #
#      Will bully you when cursed. Loves tormenting Grimm & teasing Bloom.    #
################################################################################
# Project repository: https://github.com/The-w0rst/grimmbot

import discord
from discord.ext import commands, tasks
import random
import os
import asyncio
import openai
import datetime
import logging
from config.settings import load_config, get_env_vars
from src.api_utils import ApiKeyCycle
from pathlib import Path
from src.logger import setup_logging, log_message
from src.error_handler import setup_error_handlers

# Embed color for Curse (red)
CURSE_COLOR = discord.Colour.red()


def embed_msg(text: str) -> discord.Embed:
    """Return a red embed for Curse."""
    return discord.Embed(description=text, color=CURSE_COLOR)


# Configure logging
setup_logging("curse_bot.log")
logger = logging.getLogger(__name__)
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0")) or None

# Load a single shared configuration file for all bots
ENV_PATH = Path(__file__).resolve().parent / "config" / "setup.env"
if not ENV_PATH.exists():
    raise SystemExit("config/setup.env missing. Run 'python install.py' first.")
load_config({"CURSE_DISCORD_TOKEN"})
DISCORD_TOKEN = os.getenv("CURSE_DISCORD_TOKEN")
CURSE_OPENAI_KEY = tuple(
    get_env_vars(
        "CURSE_API_KEY_1",
        "CURSE_API_KEY_2",
        "CURSE_API_KEY_3",
    )
)
CURSE_GPT_ENABLED = os.getenv("CURSE_GPT_ENABLED", "true").lower() == "true"
CURSE_OPENAI_MODEL = os.getenv("CURSE_OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_KEY_CYCLE = ApiKeyCycle(CURSE_OPENAI_KEY)


def check_required() -> None:
    missing = []
    if not os.getenv("CURSE_DISCORD_TOKEN"):
        missing.append("CURSE_DISCORD_TOKEN")
    if not any(CURSE_OPENAI_KEY):
        missing.append("CURSE_API_KEY_1")
    if missing:
        logger.error("Missing required variables: %s", ", ".join(missing))
        raise SystemExit(1)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="?", intents=intents, help_command=None)
setup_error_handlers(bot, ADMIN_USER_ID)
START_TIME = datetime.datetime.utcnow()

# === CurseBot Personality ===
curse_personality = {
    "name": "Curse",
    "role": "curse_cat",
    "traits": [
        "mischievous",
        "indifferent",
        "sassy",
        "chaotic neutral",
        "loves sushi",
        "fond of mocking cursed users",
        "rolls in tuna when no one's looking",
        "flips tail when annoyed",
    ],
    "companions": ["Grimm", "Bloom"],
}

# === Internal State ===
cursed_user_id = None
cursed_user_name = None

# === Daily Curse Scheduler ===


# Run the daily curse at noon local time
@tasks.loop(time=datetime.time(hour=12))
async def pick_daily_cursed():
    global cursed_user_id, cursed_user_name
    guild = discord.utils.get(bot.guilds)
    if not guild:
        return

    members = [m for m in guild.members if not m.bot]
    if not members:
        return

    chosen = random.choice(members)
    cursed_user_id = chosen.id
    cursed_user_name = chosen.display_name
    channel = (
        discord.utils.get(guild.text_channels, name="general") or guild.text_channels[0]
    )
    await channel.send(
        f"😼 A new curse has been cast... {cursed_user_name} is now cursed for 24 hours."
    )


# Hand out a gift at noon local time
@tasks.loop(time=datetime.time(hour=12))
async def daily_gift():
    """Give a random user a random gift from Curse."""
    guild = discord.utils.get(bot.guilds)
    if not guild:
        return
    members = [m for m in guild.members if not m.bot]
    if not members:
        return
    recipient = random.choice(members)
    gift = random.choice(gifts)
    channel = (
        discord.utils.get(guild.text_channels, name="general") or guild.text_channels[0]
    )
    if gift["positive"]:
        line = random.choice(positive_gift_responses)
    else:
        line = random.choice(negative_gift_responses)
    await channel.send(
        f"🎁 {recipient.display_name}, " + line.format(gift=gift["name"])
    )


# === Curse Interactions ===
curse_responses = [
    "You smell like expired sushi. 🤢",
    "Did you really think that would work? Cursed move.",
    "I’d help, but I’m morally opposed to effort.",
    "You're cursed. Figure it out. 😽",
    "Lick my paw and mind your business.",
    "Hope you like hairballs in your shoes.",
    "Your luck is as bad as your taste in cat food.",
    "May your pillow forever smell of catnip.",
    "Ever consider just staying quiet? We all support that idea.",
    "Did your brain take a day off or is this permanent?",
    "I've met hairballs with more charisma.",
    "You're proof that evolution can go in reverse.",
    "Keep talking, maybe eventually you'll say something smart.",
    "If laziness were an art form, you'd be a masterpiece.",
    "Somewhere a village is missing its clown.",
    "You're about as sharp as a rubber ball.",
    "Were you this annoying before the curse?",
    "If I rolled my eyes any harder, they'd fall out.",
    "You remind me why cats nap so much—so we don't have to listen.",
    "You're like a broken scratching post—useless and in the way.",
    "Why chase laser pointers when mocking you is free?",
    "You're living proof that nine lives are too many.",
    "I've heard furbies with more dignity.",
    "Bloom's sunshine is giving me migraines.",
    "Grimm could use some new bones; maybe I'll collect them.",
    "I'd chase Bloom's glitter, but I'm busy ignoring you.",
    "Grimm asked me to behave. I laughed.",
    "Your ideas are worse than Bloom's musicals.",
    "Keep pestering me and I'll curse your snacks.",
    "Grimm thinks he's scary; I'm the real nightmare.",
    "Bloom tried to pet me once. Never again.",
    "You look like you rolled in cheap catnip.",
    "I'd join Bloom's dance party, but I have dignity.",
    "Grimm scolded me again. Adorable.",
    "I only purr when plotting chaos.",
    "Bloom's cookies taste like glitter. Disgusting.",
    "Grimm's skull makes a decent bowl.",
    "You're about as fun as a damp hairball.",
    "Try me, and you'll regret it for nine lives.",
    "Bloom says I'm cute. I say she's delusional.",
    "Grimm hides his feelings, but he can't hide from me.",
    "I'm allergic to your nonsense.",
    "Bloom's hugs are a trap. Avoid at all costs.",
    "Grimm, stop acting like the boss. I'm the boss.",
    "You're not worth the litter I bury.",
    "Bloom tries so hard. It's almost sad.",
    "Grimm keeps losing his bones around me. Oops.",
    "You're as pleasant as day-old tuna.",
    "Bloom wants to sing? I'll howl instead.",
    "Grimm told me to behave; I promptly ignored him.",
    "Your voice is nails on a scratching post.",
    "Bloom's glitter is still on my fur.",
    "Grimm's jokes are as dry as his bones.",
    "Keep prying and I'll curse your microphone.",
    "Bloom won't stop with the confetti. Help.",
    "Grimm says I'm trouble. He's right.",
    "You're about as stealthy as Bloom in a tutu.",
    "I'd share my sushi, but not with you.",
    "Grimm can't control me, but he tries.",
    "Bloom, stop calling me adorable.",
    "You're one hairball away from disaster.",
    "Grimm's lectures put me to sleep.",
    "Bloom, take your bubble tea elsewhere.",
    "I'm too cool for this nonsense.",
    "Grimm owes me treats for putting up with you.",
    "Bloom still owes me a tuna roll.",
    "Don't mistake my yawn for approval.",
    "Grimm, you dropped your jawbone again.",
    "Bloom, I'm not joining your cuddle puddle.",
    "You're as exciting as stale kibble.",
    "Grimm's scythe is impressive, but my claws are sharper.",
    "Bloom can't stop talking about musicals. Spare me.",
    "One more word and I'll curse your playlist.",
    "I'd steal your soul, but it looks cheap.",
    "Grimm snores louder than you talk.",
    "Bloom's giggle makes my fur stand on end.",
    "Try me again and I'll curse your coffee.",
    "I run this squad, the others just pretend.",
]

# Short help message used by the help commands
CURSE_HELP = (
    "**CurseBot** - prefix `?`\n"
    "Try `?insult`, `?scratch @user`, `?pounce` or `?curse_me`.\n"
    "Use `?helpall` to see help for every goon."
)

GRIMM_HELP = (
    "**GrimmBot** - prefix `!`\n"
    "Try `!protectbloom`, `!roast`, `!gloom`, `!bonk` and more."
)

BLOOM_HELP = (
    "**BloomBot** - prefix `*`\n"
    "Try `*hug`, `*sing`, `*sparkle`, `*play <url>` and more."
)

# === Keywords ===
curse_keywords = {
    "grimm": [
        "Oh look, it’s the spooky skeleton again.",
        "Grimm, stop rattling around.",
        "Got bones to pick with me, Grimm?",
        "The skull king returns.",
        "Grimm, your scythe is showing.",
        "Another gloomy comment from Grimm? Shocking.",
    ],
    "bloom": [
        "Too much glitter. Not enough chaos.",
        "Bloom, take your sunshine elsewhere.",
        "If Bloom hugs me again, I'm bolting.",
        "Bloom's energy is exhausting.",
        "Another musical number, Bloom? Spare me.",
        "Bloom, you're blinding me with kindness.",
    ],
    "sushi": [
        "BACK OFF. It’s mine.",
        "Touch my sushi and face my wrath.",
        "I dream of tuna rolls.",
        "Sushi is the only good thing in life.",
        "Hands off my sashimi.",
        "Did someone say sushi? Mine.",
    ],
    "pet": [
        "Touch me and lose a finger.",
        "Pet me and face the curse.",
        "I bite those who pet without asking.",
        "Petting fee is one tuna roll.",
        "Petting rights revoked.",
        "Only Bloom can pet me—maybe.",
    ],
    "hairball": [
        "Hairball delivery incoming.",
        "Oops, hairball. Deal with it.",
    ],
    "nap": [
        "Shh, it's nap time.",
        "Wake me in an hour... maybe.",
    ],
    "curse": [
        "You rang? Someone's getting hexed.",
        "Another curse request? Fine.",
        "Curses are on sale today.",
        "Who wants a fresh hex?",
        "My curses never miss.",
        "You can't handle my curses.",
    ],
    "meow": [
        "I'm not cute. I’m cursed. Get it right.",
        "Did you just meow at me?",
        "Meow back and I'll hiss.",
        "I don't meow on command.",
        "Meowing won't save you.",
        "Only Bloom gets a purr, maybe.",
    ],
    "tuna": [
        "Step away from the tuna.",
        "Tuna is my love language.",
        "I smell tuna. Hand it over.",
        "No tuna? Then go away.",
        "Tuna tribute accepted.",
        "Keep the tuna coming.",
    ],
    "treat": [
        "No treats for you.",
        "Where are my treats?",
        "I'll trade insults for treats.",
        "Treats first, talk later.",
        "You think you deserve treats? Cute.",
        "Treats make curses better.",
    ],
    "cursed": [
        "Curse intensifies.",
        "You're cursed now, congrats.",
        "Being cursed suits you.",
        "Another soul joins the cursed ranks.",
        "Once cursed, always cursed.",
        "Feel the weight of the curse.",
    ],
}

# Gifts Curse may randomly give users once per day
gifts = [
    {"name": "a bucket of fent", "positive": False},
    {"name": "some fresh sushi", "positive": True},
    {"name": "a cursed hairball", "positive": False},
    {"name": "a shiny fish scale", "positive": True},
    {"name": "a slightly chewed toy mouse", "positive": False},
    {"name": "a jar of ghost peppers", "positive": False},
    {"name": "a mysterious paw print", "positive": False},
    {"name": "a half-empty bottle of catnip", "positive": True},
    {"name": "a tiny scythe keychain", "positive": True},
    {"name": "a worn out scratching post", "positive": False},
    {"name": "a glitter bomb from Bloom", "positive": True},
    {"name": "a sardine-scented candle", "positive": False},
    {"name": "a skeleton shaped cookie", "positive": True},
    {"name": "a bottle of midnight ink", "positive": True},
    {"name": "a creepy lullaby record", "positive": False},
    {"name": "a stack of ominous fortunes", "positive": False},
    {"name": "a black lace collar", "positive": False},
    {"name": "a box of ancient bones", "positive": False},
    {"name": "a cracked mirror shard", "positive": False},
    {"name": "a haunted feather toy", "positive": False},
    {"name": "a whispering seashell", "positive": True},
    {"name": "a mysterious potion vial", "positive": False},
    {"name": "a cursed collar bell", "positive": False},
    {"name": "a pair of glow-in-the-dark eyes", "positive": True},
    {"name": "a bag of shadow dust", "positive": False},
    {"name": "a mini spellbook", "positive": True},
    {"name": "a jar of swirling mist", "positive": False},
    {"name": "a spiky chew toy", "positive": True},
    {"name": "a midnight-blue ribbon", "positive": True},
    {"name": "a scratched-up diary", "positive": False},
    {"name": "a sinister plush bat", "positive": True},
    {"name": "a tattered pirate flag", "positive": False},
    {"name": "a small potion of mischief", "positive": True},
    {"name": "a cursed fortune cookie", "positive": False},
    {"name": "a cracked crystal ball", "positive": False},
    {"name": "a pinch of phantom fur", "positive": False},
    {"name": "a haunted treat bag", "positive": False},
    {"name": "a glow stick stash", "positive": True},
    {"name": "a vial of spooky slime", "positive": False},
    {"name": "a lock of spectral hair", "positive": False},
    {"name": "a weathered treasure map", "positive": True},
    {"name": "a bowl of strange soup", "positive": False},
    {"name": "a ball of tangled yarn", "positive": True},
    {"name": "a rogue lightning bug", "positive": True},
    {"name": "a packet of dry ice", "positive": False},
    {"name": "a cat-shaped voodoo doll", "positive": False},
    {"name": "a cursed sticker pack", "positive": False},
    {"name": "a gnarled tree branch", "positive": False},
    {"name": "a bag of sour candy", "positive": True},
    {"name": "an ominous black envelope", "positive": False},
    {"name": "a pawful of loose bolts", "positive": False},
    {"name": "a spooky origami crane", "positive": True},
    {"name": "a glow-in-the-dark collar", "positive": True},
    {"name": "a vial of cursed glitter", "positive": False},
    {"name": "a tiny haunted painting", "positive": False},
]

positive_gift_responses = [
    "Curse reluctantly gives you {gift}.",
    "With a sly grin, Curse drops {gift} in your lap.",
    "Curse acts indifferent but slides you {gift}.",
    "You receive {gift} while Curse pretends not to care.",
    "Curse gifts you {gift} and rolls his eyes.",
    "{gift} appears at your feet courtesy of Curse.",
    "Enjoy {gift}—don't say I never did anything nice.",
    "{gift} is tossed your way with a bored flick of the paw.",
]

negative_gift_responses = [
    "Curse hisses and tosses {gift} at you.",
    "You get {gift}. Curse smirks wickedly.",
    "Curse dumps {gift} on you with a laugh.",
    "{gift} hits you square in the face. Thanks, Curse.",
    "Curse sneers and shoves {gift} into your hands.",
    "A disgruntled Curse gifts you {gift}. Lucky you.",
    "{gift}? That's what you deserve, apparently.",
    "Curse hurls {gift} then walks away snickering.",
]

# Responses when the fent cloud knocks out a player
fent_player_responses = [
    "is knocked out by the fent cloud and vanishes for {minutes} minute(s).",
    "succumbs to the haze. See you in {minutes} minute(s).",
    "drops like a rock. Shadow banned for {minutes} minute(s)!",
    "coughs and fades away for {minutes} minute(s).",
    "can't handle the cloud and disappears for {minutes} minute(s).",
    "is overwhelmed and poofs for {minutes} minute(s).",
    "gets a face full of fent and dozes off for {minutes} minute(s).",
    "slinks away, cursed, for {minutes} minute(s).",
    "vanishes into the mist for {minutes} minute(s).",
    "is whisked to the shadow realm for {minutes} minute(s).",
]

# Responses when a bot gets hit by the fent cloud
fent_bot_responses = [
    "wheezes but is glad to already be dead.",
    "chuckles from beyond the grave.",
    "shrugs off the cloud—perks of undeath.",
    "mumbles that the afterlife smells better than this.",
    "laughs about undead immunity.",
    "scoffs at your attempt to harm the undead.",
    "grins—no lungs, no problem.",
    "continues haunting without pause.",
    "wonders why you bothered.",
    "licks the air and declares it spicy.",
]


# === ChatGPT Integration ===
async def chatgpt_reply(prompt: str) -> str:
    """Return a response from OpenAI in Curse's snarky style.

    Update ``CURSE_OPENAI_MODEL`` or the ``model`` argument to switch
    models like ``gpt-4o``.
    """
    if not CURSE_GPT_ENABLED:
        return "ChatGPT features are disabled."
    if not any(CURSE_OPENAI_KEY):
        return "OpenAI key missing for Curse."
    client = openai.AsyncOpenAI(api_key=OPENAI_KEY_CYCLE.next())
    try:
        response = await client.chat.completions.create(
            model=CURSE_OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Curse, a mischievous talking cat. "
                        "Reply with playful snark."
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
    check_required()
    guilds = ", ".join(g.name for g in bot.guilds)
    cogs = ", ".join(bot.cogs.keys())
    env = {
        "CURSE_DISCORD_TOKEN": (
            (DISCORD_TOKEN[:4] + "...") if DISCORD_TOKEN else "missing"
        ),
        "CURSE_OPENAI_KEY": (
            (CURSE_OPENAI_KEY[0][:4] + "...") if any(CURSE_OPENAI_KEY) else "missing"
        ),
    }
    logger.info("Curse online | guilds: %s | cogs: %s | env: %s", guilds, cogs, env)
    log_message("Curse bot ready")
    pick_daily_cursed.start()
    daily_gift.start()


@bot.event
async def on_command_error(ctx, error):
    logger.exception("Command error: %s", error)
    await ctx.send("Something broke. Check the logs.")


@bot.command(name="help")
async def help_command(ctx):
    """Show CurseBot help."""
    await ctx.send(embed=embed_msg(CURSE_HELP))


@bot.command(name="helpall")
async def help_all(ctx):
    """Show help for all bots."""
    await ctx.send(embed=embed_msg(GRIMM_HELP))
    await ctx.send(embed=embed_msg(BLOOM_HELP))
    await ctx.send(embed=embed_msg(CURSE_HELP))


@bot.command(name="menu")
async def menu(ctx):
    """Interactive menu of Curse commands."""
    commands_list = "\n".join(
        [
            "?help - show help",
            "?insult - random insult",
            "?scratch [user] - scratch someone",
            "?curse_me - embrace the curse",
        ]
    )
    await ctx.send(embed=embed_msg(commands_list))


@bot.command(name="ask")
async def ask(ctx, *, question: str):
    """Ask Curse a question via ChatGPT."""
    reply = await chatgpt_reply(question)
    for chunk in [reply[i:i + 1900] for i in range(0, len(reply), 1900)]:
        await ctx.send(chunk)


@bot.command(name="health")
async def health(ctx):
    """Report bot health statistics."""
    try:
        uptime = datetime.datetime.utcnow() - START_TIME
        latency = round(bot.latency * 1000)
        api_status = "ok" if any(CURSE_OPENAI_KEY) else "no key"
        msg = (
            f"Uptime: {uptime}\n"
            f"Ping: {latency} ms\n"
            f"Cogs: {len(bot.cogs)} loaded\n"
            f"OpenAI: {api_status}"
        )
        await ctx.send(embed=embed_msg(msg))
    except Exception as exc:
        logger.exception("health command failed: %s", exc)


@bot.command(name="status")
async def status_command(ctx):
    """Show health of all bots."""
    from src import health

    await ctx.send(embed=embed_msg(health.get_menu()))


# === Passive Comments to Cursed User ===


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.bot:
        return

    lowered = message.content.lower()

    if message.author.id == cursed_user_id:
        if random.random() < 0.2:
            await message.channel.send(
                embed=embed_msg(
                    f"{message.author.display_name}, {random.choice(curse_responses)}"
                )
            )
            return

    for trigger, responses in curse_keywords.items():
        if trigger in lowered:
            await message.channel.send(embed=embed_msg(random.choice(responses)))
            return

    await bot.process_commands(message)


# === Manual Curse Assignment ===


@bot.command()
@commands.has_permissions(administrator=True)
async def curse(ctx, member: discord.Member):
    global cursed_user_id, cursed_user_name
    cursed_user_id = member.id
    cursed_user_name = member.display_name
    await ctx.send(f"😾 Manual curse activated. {member.display_name} is now cursed.")


# === Other Commands ===


@bot.command()
async def whois_cursed(ctx):
    if cursed_user_name:
        await ctx.send(f"😼 {cursed_user_name} is still cursed... for now.")
    else:
        await ctx.send("No one's cursed. Weak.")


@bot.command()
async def sushi(ctx):
    await ctx.send("🍣 You’re not worthy of the sacred tuna.")


@bot.command()
async def flick(ctx):
    await ctx.send("*flicks tail in mild contempt*")


@bot.command()
async def insult(ctx):
    burns = [
        "You're the reason instructions exist.",
        "If I had feelings, you'd hurt them.",
        "You bring shame to sushi lovers everywhere.",
        "Your aura is soggy cardboard.",
        "You're the human equivalent of a software bug.",
        "If I wanted to hear from you, I'd hiss.",
        "You have the personality of damp bread.",
        "I'd call you dull, but that's an insult to dull things.",
        "Even my litter box smells better than your takes.",
        "I could agree with you, but then we'd both be wrong.",
        "Were you always this awkward, or is it a new talent?",
        "You're less useful than a cardboard scratching post.",
        "Your sense of humor must be on vacation.",
        "I'd tell you to go outside, but nature deserves better.",
        "I've coughed up hairballs with more wit.",
        "If ignorance was a sport, you'd take gold.",
        "You're the aftertaste of stale tuna.",
        "Even Grimm's puns are better than yours.",
        "You're proof that evolution has a sense of humor.",
        "You're about as reliable as a wet match.",
        "Even a goldfish has a longer attention span than you.",
        "You have the charisma of a wet sock.",
        "I'd explain it to you, but I left my crayons at home.",
        "Your brain called—it's taking a permanent vacation.",
        "You're proof that natural selection can take a day off.",
        "I've seen rocks with more personality.",
        "You're the human version of buffering.",
        "My scratching post has better conversation skills.",
        "You're as sharp as a marble.",
        "If laziness was an Olympic sport, you'd still come last.",
        "Your ideas are as fresh as week-old tuna.",
        "You're the reason autopilot was invented.",
        "Even a cat's hairball has more purpose.",
        "You're about as graceful as a one-legged pigeon.",
        "Your sense of direction is as lost as your logic.",
        "You give awkward a whole new meaning.",
        "I've met dust bunnies with more ambition.",
        "You're like a riddle no one wants to solve.",
        "Your best quality is your absence.",
        "You make cardboard look dynamic.",
        "I would say you're invisible, but you're more like forgettable.",
        "A doorstop has more life experience.",
        "You're about as witty as a blank notepad.",
        "Your thought process needs a reboot.",
        "You're the living proof that silence is golden.",
        "If boredom had a spokesperson, it'd be you.",
        "You're the human equivalent of a loading screen.",
        "I'd compare you to something dull, but you'd dull it further.",
        "Your attitude is as flat as day-old soda.",
        "You make monotony look exciting.",
        "You're the punchline to a joke no one told.",
        "Even my whiskers are more expressive.",
        "You're the last pick in a team of one.",
        "Your attempts at humor need a rescue mission.",
        "You're a mystery no one wants to solve.",
        "I've had naps that were more productive.",
        "You're the aftertaste of cheap kibble.",
        "Your potential is as empty as your inbox.",
        "You're a master at taking up space.",
        "You're the discount version of dull.",
        "Your cunning is as thin as watered-down milk.",
        "I'd say 'think about it,' but thinking isn't your strong suit.",
        "You're as memorable as yesterday's trash.",
        "My paw prints have more direction.",
        "You're only impressive in how unimpressive you are.",
        "You inspire me to keep napping.",
        "You're a walking talking cautionary tale.",
        "Your presence is as welcome as a sneeze in soup.",
        "If you were a page in a book, you'd be blank.",
        "Even my shadow has more depth.",
        "You're as baffling as static noise.",
        "Your track record is a straight line to nowhere.",
        "You're the footnote no one reads.",
        "Your logic is as shaky as a wobbly chair.",
        "I've met spoons with more edge.",
        "You can't even keep a goldfish entertained.",
        "You're like an ad nobody clicks.",
        "Your enthusiasm is perpetually out to lunch.",
        "You bring dullness to a whole new level.",
        "Even my leftover tuna has more zest.",
        "You're the screenshot of mediocrity.",
        "Your communication skills need subtitles.",
        "You put the 'meh' in meh-diocre.",
        "You're the only glitch in your own system.",
        "I've seen snails with more urgency.",
        "You're as bright as a burnt-out bulb.",
        "Your only strategy is no strategy.",
        "You have the reliability of a broken compass.",
        "You're a standing ovation for boredom.",
        "Your brilliance could fill a thimble, maybe.",
        "I've witnessed statues with more spontaneity.",
        "You're as interesting as watching paint stay the same color.",
        "You have the creativity of a blank screen.",
        "Your ambition forgot to show up.",
        "You're the leftover crust nobody wants.",
        "Your ability to disappoint is unmatched.",
        "You turned potential into a ghost town.",
        "You're the poster child for underwhelming.",
        "Even my yawns are more exciting than you.",
    ]
    await ctx.send(random.choice(burns))


@bot.command()
async def hiss(ctx):
    await ctx.send("Hissss! Keep your distance.")


@bot.command()
async def scratch(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"*scratches {member.display_name} just because*")


@bot.command()
async def pet(ctx):
    """Attempt to pet Curse."""
    global cursed_user_id, cursed_user_name
    outcome = random.random()
    if outcome < 0.33:
        await ctx.send(
            "😼 Curse hurls a fent brick into the ceiling fan! A cloud of fent fills the room."
        )
        for member in ctx.guild.members:
            if member == bot.user:
                continue
            if member.status == discord.Status.offline:
                continue
            if random.random() < 0.5:
                if member.bot:
                    await ctx.send(
                        f"{member.display_name} {random.choice(fent_bot_responses)}"
                    )
                else:
                    minutes = random.randint(1, 3)
                    await ctx.send(
                        f"{member.display_name} "
                        f"{random.choice(fent_player_responses).format(minutes=minutes)}"
                    )
    elif outcome < 0.66:
        await ctx.send("😼 *purrs softly* Maybe I'll spare you... for now.")
    else:
        await ctx.send(
            f"*scratches {ctx.author.display_name} and hisses.* You're cursed now!"
        )
        cursed_user_id = ctx.author.id
        cursed_user_name = ctx.author.display_name
        try:
            await ctx.author.edit(nick=f"Cursed {ctx.author.display_name}")
        except discord.Forbidden:
            pass
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name="Cursed")
        if role is None:
            role = await guild.create_role(
                name="Cursed", colour=discord.Colour.purple()
            )
        try:
            await ctx.author.add_roles(role)
        except discord.Forbidden:
            pass


@bot.command()
async def curse_me(ctx):
    global cursed_user_id, cursed_user_name
    cursed_user_id = ctx.author.id
    cursed_user_name = ctx.author.display_name
    await ctx.send(f"😾 Fine. {ctx.author.display_name} is now cursed.")


@bot.command(name="judge")
@commands.cooldown(1, 60, commands.BucketType.user)
async def judge(ctx, other: discord.Member, *, issue: str):
    """Ask Curse to judge an argument."""
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
        "Give your verdict in character as Curse."
    )
    reply = await chatgpt_reply(prompt)
    for chunk in [reply[i:i + 1900] for i in range(0, len(reply), 1900)]:
        await ctx.send(chunk)


@bot.command()
async def hairball(ctx):
    """Share a lovely hairball."""
    await ctx.send("*coughs up a hairball on your shoes*")


@bot.command()
async def pounce(ctx, member: discord.Member | None = None):
    """Pounce on someone."""
    member = member or ctx.author
    await ctx.send(f"*pounces on {member.display_name} unexpectedly*")


@bot.command()
async def nap(ctx):
    """Announce that Curse is taking a nap."""
    await ctx.send("😼 Curling up for a nap. Don't bother me.")


check_required()
try:
    bot.run(DISCORD_TOKEN)
finally:
    log_message("Curse shutting down")
