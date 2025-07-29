import discord
from discord.ext import commands, tasks
import random
import os

import socketio

COG_VERSION = "1.4"

# Environment values are read from the parent process
DISCORD_TOKEN = os.getenv("GRIMM_DISCORD_TOKEN")
GRIMM_API_KEY_1 = os.getenv("GRIMM_API_KEY_1")
GRIMM_API_KEY_2 = os.getenv("GRIMM_API_KEY_2")
GRIMM_API_KEY_3 = os.getenv("GRIMM_API_KEY_3")
SOCKET_SERVER = os.getenv("SOCKET_SERVER_URL", "http://localhost:5000")

sio = socketio.Client()
try:
    sio.connect(SOCKET_SERVER)
except Exception as e:
    print(f"Failed to connect to Socket.IO dashboard: {e}")


def send_status(status, message):
    try:
        sio.emit("bot_status", {"bot": "Grimm", "status": status, "message": message})
    except Exception as e:
        print(f"SocketIO error: {e}")


class GrimmCog(commands.Cog):
    """GrimmBot personality packaged as a Cog. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_interactions = {}
        self.gifts = [
            {"name": "a polished bone charm", "positive": True},
            {"name": "a dusty old cloak", "positive": False},
            {"name": "a jar of graveyard soil", "positive": False},
            {"name": "a sharpened mini scythe", "positive": True},
            {"name": "a gloom-infused candle", "positive": False},
            {"name": "a protective talisman", "positive": True},
            {"name": "a cracked skull mug", "positive": True},
            {"name": "a batch of burnt cookies from Bloom", "positive": False},
            {"name": "a heavy tome of doom", "positive": False},
            {"name": "a friendly pat on the back", "positive": True},
            {"name": "a vial of shadow essence", "positive": False},
            {"name": "a weathered grave map", "positive": False},
            {"name": "a chilled bottle of ectoplasm", "positive": True},
            {"name": "a shard of night crystal", "positive": False},
            {"name": "a carved bone whistle", "positive": True},
            {"name": "a jar of fake cobwebs", "positive": False},
            {"name": "a rusted lock and key", "positive": False},
            {"name": "a midnight raven feather", "positive": True},
            {"name": "a set of polished teeth", "positive": False},
            {"name": "a cursed coin", "positive": False},
            {"name": "a skeletal hand bookmark", "positive": True},
            {"name": "a gloomcore mixtape", "positive": True},
            {"name": "a wilted black rose", "positive": False},
            {"name": "a phantasmal charm bracelet", "positive": True},
            {"name": "a spider silk pouch", "positive": False},
            {"name": "a pair of cracked goggles", "positive": False},
            {"name": "a cryptic warning note", "positive": False},
            {"name": "a gloom-themed sticker pack", "positive": True},
            {"name": "a chipped obsidian ring", "positive": True},
            {"name": "a haunted mirror fragment", "positive": False},
            {"name": "a pocket-sized skull", "positive": True},
            {"name": "a dusty rattle", "positive": False},
            {"name": "a frayed reaper cloak scrap", "positive": False},
            {"name": "a bone-carved dice set", "positive": True},
            {"name": "a gloom-forged brooch", "positive": True},
            {"name": "a jar of spectral fog", "positive": False},
            {"name": "a tattered wanted poster", "positive": False},
            {"name": "a protective rune stone", "positive": True},
            {"name": "a pair of ominous candles", "positive": False},
            {"name": "a small coffin-shaped box", "positive": True},
            {"name": "a reaper emblem patch", "positive": True},
            {"name": "a cracked hourglass", "positive": False},
            {"name": "a ghostly lullaby sheet", "positive": True},
            {"name": "a gloom-infused quill", "positive": True},
            {"name": "a bottle of midnight oil", "positive": False},
            {"name": "a faintly glowing skull ring", "positive": True},
            {"name": "a pack of doom-themed cards", "positive": True},
            {"name": "a haunting melody box", "positive": True},
            {"name": "a rusty chain link", "positive": False},
            {"name": "a gloom-ward amulet", "positive": True},
        ]
        self.positive_gift_responses = [
            "Grimm grumbles but offers {gift}.",
            "With a hint of kindness, Grimm hands you {gift}.",
            "Grimm nods solemnly and gives you {gift}.",
        ]
        self.negative_gift_responses = [
            "Grimm tosses {gift} at your feet with disdain.",
            "Without much care, Grimm drops {gift} near you.",
            "Grimm sighs heavily and gifts you {gift}.",
        ]
        self.daily_gift.start()

    @tasks.loop(hours=24)
    async def daily_gift(self):
        """Give a random user a Grimm-style gift."""
        guild = discord.utils.get(self.bot.guilds)
        if not guild:
            return
        members = [m for m in guild.members if not m.bot]
        if not members:
            return
        recipient = random.choice(members)
        interactions = self.user_interactions.get(recipient.id, 0)
        positive = interactions >= 5
        choices = [g for g in self.gifts if g["positive"] == positive]
        gift = random.choice(choices)
        channel = (
            discord.utils.get(guild.text_channels, name="general")
            or guild.text_channels[0]
        )
        if positive:
            line = random.choice(self.positive_gift_responses)
            await self.apply_positive_effect(recipient)
        else:
            line = random.choice(self.negative_gift_responses)
            await self.apply_negative_effect(recipient)
        await channel.send(
            f"🎁 {recipient.display_name}, " + line.format(gift=gift["name"])
        )

    async def apply_positive_effect(self, member: discord.Member):
        guild = member.guild
        role = discord.utils.get(guild.roles, name="Grimm's Shield")
        if role is None:
            role = await guild.create_role(
                name="Grimm's Shield", colour=discord.Colour.dark_gray()
            )
        try:
            await member.add_roles(role)
        except discord.Forbidden:
            pass

    async def apply_negative_effect(self, member: discord.Member):
        role = discord.utils.get(member.guild.roles, name="Grimm's Shield")
        if role:
            try:
                await member.remove_roles(role)
            except discord.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_ready(self):
        print("Grimm cog loaded.")
        send_status("online", "On patrol. Nobody dies on my watch (except Mondays).")

    @commands.command()
    async def protectbloom(self, ctx):
        """Grimm stands guard for Bloom."""
        responses = [
            "Back off. The flower stays safe with me. 🪦🛡️",
            "I’m watching you. Touch Bloom and you deal with me.",
            "Step away from the cutesy one, or meet your fate.",
        ]
        await ctx.send(random.choice(responses))
        send_status("active", "Protected Bloom.")

    @commands.command()
    async def roast(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        burns = [
            f"{member.mention}, you're not even worth the trouble.",
            f"{member.mention}, if I had a nickel for every brain cell you lost, I’d be immortal.",
            f"{member.mention}, some people were born to goon. You were born to be gooned on.",
        ]
        await ctx.send(random.choice(burns))
        send_status("active", f"Roasted {member.display_name}")

    @commands.command()
    async def goon(self, ctx):
        responses = [
            "Who called the goon squad? Oh, it was just you.",
            "Goons assemble. And by goons, I mean the rest of you.",
            "This is my squad, you’re just visiting.",
        ]
        await ctx.send(random.choice(responses))
        send_status("active", "Issued goon decree.")

    @commands.command()
    async def ominous(self, ctx):
        responses = [
            "I hear footsteps... they're yours.",
            "Sometimes I let people think they’re safe.",
            "Death is just a punchline you don’t want to hear.",
        ]
        await ctx.send(random.choice(responses))
        send_status("active", "Dropped an ominous hint.")

    @commands.command(name="grimm_bloom")
    async def bloom(self, ctx):
        responses = [
            "If you see Bloom, tell her I’m not worried about her. At all. Not even a little. 🖤",
            "She's a handful, but she’s my handful.",
            "Don’t let the cutesy act fool you. She’s the real trouble.",
        ]
        await ctx.send(random.choice(responses))
        send_status("active", "Talked about Bloom.")

    @commands.command(name="grimm_curse")
    async def curse(self, ctx):
        responses = [
            "That cat is trouble on four paws.",
            "If you see Curse, hide the sushi and your pride.",
            "I let Curse think he's in charge sometimes. It keeps the peace.",
        ]
        await ctx.send(random.choice(responses))
        send_status("active", "Mocked Curse.")

    @commands.command()
    async def scythe(self, ctx):
        await ctx.send("⚰️ *Swings the scythe dramatically, but misses on purpose.*")

    @commands.command()
    async def shadow(self, ctx):
        await ctx.send("*You feel a cold chill. Grimm winks.*")

    @commands.command()
    async def flip(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f"{member.mention}, you just got goon-flipped. 😈")
        send_status("active", f"Flipped off {member.display_name}")

    @commands.command()
    async def nickname(self, ctx, member: discord.Member = None):
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
        ]
        await ctx.send(f"{member.mention}, you're a {random.choice(names)}.")
        send_status("active", f"Called {member.display_name} a nickname")

    @commands.command()
    async def brood(self, ctx):
        await ctx.send("*broods quietly in a dark corner*")

    @commands.command()
    async def bone(self, ctx):
        await ctx.send("You want a bone? I'm using all of mine.")

    @commands.command()
    async def doom(self, ctx):
        """Announce an ominous countdown to doom."""
        hours = random.randint(1, 24)
        await ctx.send(f"Doom arrives in {hours} hours. Or not. We'll see.")

    @commands.command()
    async def guard(self, ctx, member: discord.Member | None = None):
        """Grimm stands guard for the specified member."""
        member = member or ctx.author
        await ctx.send(
            f"Standing guard for {member.display_name}. Nothing gets past me."
        )

    @commands.command()
    async def haunt(self, ctx, member: discord.Member | None = None):
        """Playfully haunt a user."""
        member = member or ctx.author
        await ctx.send(f"*haunts {member.display_name} for fun*")

    @commands.command()
    async def shield(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        shields = [
            f"{member.mention}, no harm comes to you on my watch. (Except embarrassment.)",
            f"Stand behind me, {member.mention}. The goon squad’s got you.",
            f"{member.mention}, if anyone messes with you, send them to me.",
        ]
        await ctx.send(random.choice(shields))
        send_status("active", f"Shielded {member.display_name}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        self.user_interactions[message.author.id] = (
            self.user_interactions.get(message.author.id, 0) + 1
        )
        lowered = message.content.lower()
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
        for trigger, responses in keywords.items():
            if trigger in lowered:
                await message.channel.send(random.choice(responses))
                send_status("active", f"Reacted to {trigger} mention.")
                return

        if "bloom" in lowered and random.random() < 0.18:
            await message.channel.send(
                "Someone said Bloom? She’s probably off singing again..."
            )
            send_status("active", "Reacted to Bloom mention.")
        elif "curse" in lowered and random.random() < 0.18:
            await message.channel.send("I told you, don’t trust the cat. Ever.")
            send_status("active", "Reacted to Curse mention.")

        if random.random() < 0.05:
            grimm_responses = [
                "What now?",
                "I'm not angry, just disappointed... again.",
                "Keep it down. I'm trying to brood.",
                "Don't tell Bloom, but I'm glad you're here.",
                "Curse, stop clawing the furniture.",
                "Sigh. Another day, another bit of chaos.",
            ]
            await message.channel.send(random.choice(grimm_responses))


async def setup(bot: commands.Bot):
    """Load the cog."""
    await bot.add_cog(GrimmCog(bot))
