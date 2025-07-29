from discord.ext import commands
from src import health

COG_VERSION = "1.0"

class HealthCog(commands.Cog):
    """Shared health menu commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="health")
    async def health_cmd(self, ctx: commands.Context):
        """Show current health for all bots."""
        await ctx.send(health.get_menu())

async def setup(bot: commands.Bot):
    await bot.add_cog(HealthCog(bot))
