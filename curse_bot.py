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

import discord
from discord.ext import commands, tasks
import random
import os
from dotenv import load_dotenv

# Load a single shared configuration file for all bots
load_dotenv("config/setup.env")
DISCORD_TOKEN = os.getenv("CURSE_DISCORD_TOKEN")
CURSE_API_KEY_1 = os.getenv("CURSE_API_KEY_1")
CURSE_API_KEY_2 = os.getenv("CURSE_API_KEY_2")
CURSE_API_KEY_3 = os.getenv("CURSE_API_KEY_3")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

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
        "flips tail when annoyed"
    ],
    "companions": ["Grimm", "Bloom"]
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
    channel = discord.utils.get(guild.text_channels, name="general") or guild.text_channels[0]
    await channel.send(f"😼 A new curse has been cast... {cursed_user_name} is now cursed for 24 hours.")

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
    "I've heard furbies with more dignity."
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
    "cursed": ["Curse intensifies."]
}

# === On Ready ===
@bot.event
async def on_ready():
    print(f"{curse_personality['name']} is here to ruin someone's day.")
    pick_daily_cursed.start()

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
            await message.channel.send(f"{message.author.display_name}, {random.choice(curse_responses)}")
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
        "I'd tell you to go outside, but nature deserves better."
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
async def curse_me(ctx):
    global cursed_user_id, cursed_user_name
    cursed_user_id = ctx.author.id
    cursed_user_name = ctx.author.display_name
    await ctx.send(f"😾 Fine. {ctx.author.display_name} is now cursed.")

bot.run(DISCORD_TOKEN)
