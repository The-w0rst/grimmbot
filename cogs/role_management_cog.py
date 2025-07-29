import discord
from discord.ext import commands

COG_VERSION = "1.0"


class RoleManagementCog(commands.Cog):
    """Commands for managing roles."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, name: str, color: discord.Color | None = None):
        """Create a new role."""
        await ctx.guild.create_role(name=name, colour=color or discord.Color.default())
        await ctx.send(f"Role `{name}` created.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def deleterole(self, ctx, role: discord.Role):
        """Delete a role."""
        await role.delete()
        await ctx.send(f"Deleted role {role.name}.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def giverole(self, ctx, member: discord.Member, role: discord.Role):
        """Give a member a role."""
        await member.add_roles(role)
        await ctx.send(f"Gave {role.name} to {member.display_name}.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, member: discord.Member, role: discord.Role):
        """Remove a role from a member."""
        await member.remove_roles(role)
        await ctx.send(f"Removed {role.name} from {member.display_name}.")


async def setup(bot: commands.Bot):
    await bot.add_cog(RoleManagementCog(bot))
