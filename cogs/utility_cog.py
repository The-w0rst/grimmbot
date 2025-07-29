import discord
from discord.ext import commands

COG_VERSION = "1.0"


class UtilityCog(commands.Cog):
    """General info commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member | None = None):
        """Display information about a member."""
        member = member or ctx.author
        embed = discord.Embed(title="User Info", color=member.color)
        embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
        embed.add_field(name="ID", value=str(member.id))
        embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"))
        roles = [r.name for r in member.roles if r != ctx.guild.default_role]
        embed.add_field(name="Roles", value=", ".join(roles) or "None", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        """Display server statistics."""
        guild = ctx.guild
        embed = discord.Embed(title=guild.name, color=discord.Color.blue())
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"))
        embed.add_field(name="Owner", value=str(guild.owner))
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member | None = None):
        """Show a user's avatar URL."""
        member = member or ctx.author
        await ctx.send(member.display_avatar.url)


async def setup(bot: commands.Bot):
    await bot.add_cog(UtilityCog(bot))
