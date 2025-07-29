from discord.ext import commands

COG_VERSION = "1.5"


class PollsCog(commands.Cog):
    """Quick reaction polls. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, *, question: str):
        """Start a yes/no poll."""
        msg = await ctx.send(
            f"\N{BAR CHART} **{question}**\nReact with \U0001f44d or \U0001f44e"
        )
        await msg.add_reaction("\U0001f44d")
        await msg.add_reaction("\U0001f44e")


async def setup(bot: commands.Bot):
    await bot.add_cog(PollsCog(bot))
