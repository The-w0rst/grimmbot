import discord
from discord.ext import commands, tasks
import random
import os
from dotenv import load_dotenv
from pathlib import Path

# Load a single shared configuration file for all bots
ENV_PATH = Path(__file__).resolve().parents[1] / "config" / "setup.env"
load_dotenv(ENV_PATH)
DISCORD_TOKEN = os.getenv("CURSE_DISCORD_TOKEN")
CURSE_API_KEY_1 = os.getenv("CURSE_API_KEY_1")
CURSE_API_KEY_2 = os.getenv("CURSE_API_KEY_2")
CURSE_API_KEY_3 = os.getenv("CURSE_API_KEY_3")


class CurseCog(commands.Cog):
    """CurseBot personality packaged as a Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cursed_user_id = None
        self.cursed_user_name = None
        self.curse_responses = [
            "You smell like expired sushi. 🤢",
            "Did you really think that would work? Cursed move.",
            "I’d help, but I’m morally opposed to effort.",
            "You're cursed. Figure it out. 😽",
            "Lick my paw and mind your business.",
            "Hope you like hairballs in your shoes.",
            "Your luck is as bad as your taste in cat food.",
            "May your pillow forever smell of catnip."
        ]
        self.curse_keywords = {
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
        self.pick_daily_cursed.start()

    @tasks.loop(hours=24)
    async def pick_daily_cursed(self):
        guild = discord.utils.get(self.bot.guilds)
        if not guild:
            return
        members = [m for m in guild.members if not m.bot]
        if not members:
            return
        chosen = random.choice(members)
        self.cursed_user_id = chosen.id
        self.cursed_user_name = chosen.display_name
        channel = discord.utils.get(
            guild.text_channels, name="general") or guild.text_channels[0]
        await channel.send(f"😼 A new curse has been cast... {self.cursed_user_name} is now cursed for 24 hours.")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Curse cog loaded.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        lowered = message.content.lower()
        if message.author.id == self.cursed_user_id and random.random() < 0.2:
            await message.channel.send(f"{message.author.display_name}, {random.choice(self.curse_responses)}")
            return
        for trigger, responses in self.curse_keywords.items():
            if trigger in lowered:
                await message.channel.send(random.choice(responses))
                return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def curse(self, ctx, member: discord.Member):
        self.cursed_user_id = member.id
        self.cursed_user_name = member.display_name
        await ctx.send(f"😾 Manual curse activated. {member.display_name} is now cursed.")

    @commands.command()
    async def whois_cursed(self, ctx):
        if self.cursed_user_name:
            await ctx.send(f"😼 {self.cursed_user_name} is still cursed... for now.")
        else:
            await ctx.send("No one's cursed. Weak.")

    @commands.command()
    async def sushi(self, ctx):
        await ctx.send("🍣 You’re not worthy of the sacred tuna.")

    @commands.command()
    async def flick(self, ctx):
        await ctx.send("*flicks tail in mild contempt*")

    @commands.command()
    async def insult(self, ctx):
        burns = [
            "You're the reason instructions exist.",
            "If I had feelings, you'd hurt them.",
            "You bring shame to sushi lovers everywhere.",
            "Your aura is soggy cardboard."
        ]
        await ctx.send(random.choice(burns))

    @commands.command()
    async def hiss(self, ctx):
        await ctx.send("Hissss! Keep your distance.")

    @commands.command()
    async def scratch(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f"*scratches {member.display_name} just because*")

    @commands.command()
    async def pet(self, ctx):
        """Attempt to pet Curse."""
        if random.random() < 0.5:
            await ctx.send("😼 *purrs softly* Maybe I'll spare you... for now.")
        else:
            await ctx.send(
                f"*scratches {ctx.author.display_name} and hisses.* You're cursed now!"
            )
            self.cursed_user_id = ctx.author.id
            self.cursed_user_name = ctx.author.display_name
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

    @commands.command()
    async def curse_me(self, ctx):
        self.cursed_user_id = ctx.author.id
        self.cursed_user_name = ctx.author.display_name
        await ctx.send(f"😾 Fine. {ctx.author.display_name} is now cursed.")

    @commands.command()
    async def hairball(self, ctx):
        """Share a lovely hairball."""
        await ctx.send("*coughs up a hairball on your shoes*")

    @commands.command()
    async def pounce(self, ctx, member: discord.Member | None = None):
        """Pounce on someone."""
        member = member or ctx.author
        await ctx.send(f"*pounces on {member.display_name} unexpectedly*")

    @commands.command()
    async def nap(self, ctx):
        """Announce that Curse is taking a nap."""
        await ctx.send("😼 Curling up for a nap. Don't bother me.")


async def setup(bot: commands.Bot):
    """Load the cog."""
    await bot.add_cog(CurseCog(bot))
