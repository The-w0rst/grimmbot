import discord
from discord.ext import commands


from . import grimm_utils

COG_VERSION = "1.5"


class GrimmExtraCog(commands.Cog):
    """Additional utilities and fun commands for Grimm. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def gloom(self, ctx):
        """Check Grimm's current gloom level."""
        level = grimm_utils.gloom_level()
        if level >= 70:
            mood = "The shadows gather. Grimm is pleased."
        elif level >= 40:
            mood = "Decently gloomy. Could be worse."
        else:
            mood = "Too bright for Grimm's taste."
        await ctx.send(f"Gloom level: {level}/100. {mood}")

    @commands.command()
    async def lament(self, ctx):
        """Share one of Grimm's gloomy laments."""
        await ctx.send(grimm_utils.random_lament())

    @commands.command()
    async def bonk(self, ctx, member: discord.Member | None = None):
        """Bonk a member with Grimm's trusty femur."""
        member = member or ctx.author
        await ctx.send(f"*bonks {member.display_name} on the head with a femur*")

    @commands.command(name="inventory")
    async def show_inventory(self, ctx):
        """Display a random item from Grimm's stash."""
        item = grimm_utils.random_item()
        await ctx.send(f"Grimm hands you {item}.")


async def setup(bot: commands.Bot):
    await bot.add_cog(GrimmExtraCog(bot))
