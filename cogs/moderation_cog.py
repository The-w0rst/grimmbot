import discord
from discord.ext import commands
import datetime

COG_VERSION = "1.4"


class ModerationCog(commands.Cog):
    """Basic moderation commands. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.warnings: dict[int, int] = {}
        self.blacklist = {"badword"}

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, seconds: int, *, reason: str | None = None):
        """Temporarily mute a member."""
        try:
            await member.timeout(datetime.timedelta(seconds=seconds), reason=reason)
            await ctx.send(f"Muted {member.display_name} for {seconds} seconds.")
        except Exception:
            await ctx.send("Failed to mute.")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str | None = None):
        """Warn a member and track warning count."""
        count = self.warnings.get(member.id, 0) + 1
        self.warnings[member.id] = count
        await ctx.send(f"Warned {member.display_name}. Total warnings: {count}")

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

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return
        if any(word in message.content.lower() for word in self.blacklist):
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} watch your language!",
                delete_after=5,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(ModerationCog(bot))
