from discord.ext import commands

COG_VERSION = "1.4"


class PollsCog(commands.Cog):
    """Quick reaction polls. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, *, question: str):
        """Start a yes/no poll."""
        msg = await ctx.send(
            f"\N{BAR CHART} **{question}**\nReact with \U0001F44D or \U0001F44E"
        )
        await msg.add_reaction("\U0001F44D")
        await msg.add_reaction("\U0001F44E")


async def setup(bot: commands.Bot):
    await bot.add_cog(PollsCog(bot))
