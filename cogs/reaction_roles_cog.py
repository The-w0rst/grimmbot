import discord
from discord.ext import commands

COG_VERSION = "1.5"


class ReactionRolesCog(commands.Cog):
    """Self-assign roles via reactions. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.message_roles: dict[int, int] = {}

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def reactrole(self, ctx, role: discord.Role, *, text: str):
        msg = await ctx.send(text)
        await msg.add_reaction("\u2705")
        self.message_roles[msg.id] = role.id

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id not in self.message_roles or payload.member.bot:
            return
        role_id = self.message_roles[payload.message_id]
        guild = self.bot.get_guild(payload.guild_id)
        role = guild.get_role(role_id)
        if role:
            await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.message_id not in self.message_roles:
            return
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if not member or member.bot:
            return
        role_id = self.message_roles[payload.message_id]
        role = guild.get_role(role_id)
        if role:
            await member.remove_roles(role)


async def setup(bot: commands.Bot):
    await bot.add_cog(ReactionRolesCog(bot))
