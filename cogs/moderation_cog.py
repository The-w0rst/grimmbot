
import discord
from discord.ext import commands
COG_VERSION = "1.1"


class ModerationCog(commands.Cog):
    """Basic moderation commands. Version 1.1."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str | None = None):
        """Kick a member from the server."""
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.display_name}.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str | None = None):
        """Ban a member from the server."""
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.display_name}.")

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        """Delete a number of recent messages."""
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Deleted {len(deleted)-1} messages.", delete_after=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(ModerationCog(bot))
