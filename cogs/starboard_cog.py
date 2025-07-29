import discord
from discord.ext import commands

COG_VERSION = "1.5"


class StarboardCog(commands.Cog):
    """Save popular messages to a starboard channel. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.threshold = 3
        self.starboard_cache: set[int] = set()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if str(payload.emoji) != "\u2b50":
            return
        if payload.message_id in self.starboard_cache:
            return
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if sum(
            1
            for r in message.reactions
            if str(r.emoji) == "\u2b50" and r.count >= self.threshold
        ):
            starboard = discord.utils.get(channel.guild.text_channels, name="starboard")
            if not starboard:
                return
            embed = discord.Embed(
                description=message.content, color=discord.Color.gold()
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            embed.timestamp = message.created_at
            await starboard.send(embed=embed)
            self.starboard_cache.add(payload.message_id)


async def setup(bot: commands.Bot):
    await bot.add_cog(StarboardCog(bot))
