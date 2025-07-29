import asyncio
from discord.ext import commands

COG_VERSION = "1.4"


class ReminderCog(commands.Cog):
    """User reminders and timers. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="remindme")
    async def remindme(self, ctx, seconds: int, *, text: str):
        """Remind the user after a number of seconds."""
        await ctx.send(f"I'll remind you in {seconds} seconds.")
        await asyncio.sleep(seconds)
        try:
            await ctx.author.send(f"Reminder: {text}")
        except Exception:
            await ctx.send(f"{ctx.author.mention} Reminder: {text}")


async def setup(bot: commands.Bot):
    await bot.add_cog(ReminderCog(bot))
