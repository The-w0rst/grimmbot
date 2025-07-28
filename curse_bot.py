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

load_dotenv()
DISCORD_TOKEN = os.getenv("CURSE_DISCORD_TOKEN")

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
    "Lick my paw and mind your business."
]

# === Keywords ===
curse_keywords = {
    "grimm": ["Oh look, it’s the spooky skeleton again."],
    "bloom": ["Too much glitter. Not enough chaos."],
    "sushi": ["BACK OFF. It’s mine."],
    "pet": ["Touch me and lose a finger."],
    "curse": ["You rang? Someone's getting hexed."],
    "meow": ["I'm not cute. I’m cursed. Get it right."]
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
        "Your aura is soggy cardboard." 
    ]
    await ctx.send(random.choice(burns))

bot.run(DISCORD_TOKEN)
