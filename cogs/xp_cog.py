import discord
from discord.ext import commands

COG_VERSION = "1.4"


class XPCog(commands.Cog):
    """Simple chat-based XP and leveling. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.xp: dict[int, int] = {}

    def _level(self, xp: int) -> int:
        return int(xp ** 0.5)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return
        user_id = message.author.id
        self.xp[user_id] = self.xp.get(user_id, 0) + 1

    @commands.command()
    async def rank(self, ctx, member: discord.Member | None = None):
        member = member or ctx.author
        xp = self.xp.get(member.id, 0)
        level = self._level(xp)
        await ctx.send(f"{member.display_name} is level {level} with {xp} XP.")

    @commands.command()
    async def leaderboard(self, ctx):
        if not self.xp:
            await ctx.send("Nobody has XP yet.")
            return
        top = sorted(self.xp.items(), key=lambda kv: kv[1], reverse=True)[:5]
        lines = []
        for idx, (uid, xp) in enumerate(top, 1):
            member = ctx.guild.get_member(uid)
            name = member.display_name if member else str(uid)
            lines.append(f"{idx}. {name} - {xp} XP")
        await ctx.send("Leaderboard:\n" + "\n".join(lines))


async def setup(bot: commands.Bot):
    await bot.add_cog(XPCog(bot))
