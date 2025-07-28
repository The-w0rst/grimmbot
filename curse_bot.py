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
from dotenv import load_dotenv
from pathlib import Path

# Load a single shared configuration file for all bots
ENV_PATH = Path(__file__).resolve().parent / "config" / "setup.env"
if not ENV_PATH.exists():
    raise SystemExit("config/setup.env missing. Run 'python install.py' first.")
load_dotenv(ENV_PATH)
DISCORD_TOKEN = os.getenv("CURSE_DISCORD_TOKEN")
CURSE_API_KEY_1 = os.getenv("CURSE_API_KEY_1")
CURSE_API_KEY_2 = os.getenv("CURSE_API_KEY_2")
CURSE_API_KEY_3 = os.getenv("CURSE_API_KEY_3")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)

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


@tasks.loop(hours=24)
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


@tasks.loop(hours=24)
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
    await channel.send(f"🎁 {recipient.display_name}, " + line.format(gift=gift["name"]))


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
]

# === Keywords ===
curse_keywords = {
    "grimm": ["Oh look, it’s the spooky skeleton again."],
    "bloom": ["Too much glitter. Not enough chaos."],
    "sushi": ["BACK OFF. It’s mine."],
    "pet": ["Touch me and lose a finger."],
    "curse": ["You rang? Someone's getting hexed."],
    "meow": ["I'm not cute. I’m cursed. Get it right."],
    "tuna": ["Step away from the tuna."],
    "treat": ["No treats for you."],
    "cursed": ["Curse intensifies."],
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
]

positive_gift_responses = [
    "Curse reluctantly gives you {gift}.",
    "With a sly grin, Curse drops {gift} in your lap.",
    "Curse acts indifferent but slides you {gift}.",
]

negative_gift_responses = [
    "Curse hisses and tosses {gift} at you.",
    "You get {gift}. Curse smirks wickedly.",
    "Curse dumps {gift} on you with a laugh.",
]

# === On Ready ===


@bot.event
async def on_ready():
    print(f"{curse_personality['name']} is here to ruin someone's day.")
    pick_daily_cursed.start()
    daily_gift.start()


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
                f"{message.author.display_name}, {random.choice(curse_responses)}"
            )
            return

    for trigger, responses in curse_keywords.items():
        if trigger in lowered:
            await message.channel.send(random.choice(responses))
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
    if random.random() < 0.5:
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


if not DISCORD_TOKEN:
    raise RuntimeError("CURSE_DISCORD_TOKEN not set in config/setup.env")
bot.run(DISCORD_TOKEN)
