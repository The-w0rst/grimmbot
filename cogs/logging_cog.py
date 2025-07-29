import discord
from discord.ext import commands

COG_VERSION = "1.4"


class LoggingCog(commands.Cog):
    """Log joins, leaves, and message edits/deletes. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _log(self, guild: discord.Guild, text: str):
        channel = discord.utils.get(guild.text_channels, name="bot-logs")
        if channel:
            await channel.send(text)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await self._log(member.guild, f"Member joined: {member.display_name}")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await self._log(member.guild, f"Member left: {member.display_name}")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.guild:
            await self._log(message.guild, f"Message deleted in {message.channel}: {message.author.display_name}: {message.content}")

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.guild and before.content != after.content:
            await self._log(before.guild, f"Message edited in {before.channel}: {before.author.display_name}: {before.content} -> {after.content}")


async def setup(bot: commands.Bot):
    await bot.add_cog(LoggingCog(bot))
