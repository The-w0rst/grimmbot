from discord.ext import commands
from pathlib import Path

LOG_PATH = Path("logs/activity.log")


class AuditCog(commands.Cog):
    """Commands for viewing recent bot actions."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def audit(self, ctx, lines: int = 10):
        """Show the last few actions from the activity log."""
        if not LOG_PATH.exists():
            await ctx.send("No activity recorded yet.")
            return
        data = LOG_PATH.read_text().splitlines()[-lines:]
        output = "\n".join(data) or "No recent activity"
        await ctx.send(f"```\n{output}\n```")


async def setup(bot: commands.Bot):
    await bot.add_cog(AuditCog(bot))
