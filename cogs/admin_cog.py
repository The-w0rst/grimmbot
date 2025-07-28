from discord.ext import commands


class AdminCog(commands.Cog):
    """Administration utilities for managing cogs."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        """Load a cog by its module name."""
        ext = f"cogs.{cog}"
        try:
            await self.bot.load_extension(ext)
            await ctx.send(f"Loaded {ext}")
        except Exception as e:
            await ctx.send(f"Failed to load {ext}: {e}")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
        """Unload a cog."""
        ext = f"cogs.{cog}"
        try:
            await self.bot.unload_extension(ext)
            await ctx.send(f"Unloaded {ext}")
        except Exception as e:
            await ctx.send(f"Failed to unload {ext}: {e}")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        """Reload a cog."""
        ext = f"cogs.{cog}"
        try:
            await self.bot.reload_extension(ext)
            await ctx.send(f"Reloaded {ext}")
        except Exception as e:
            await ctx.send(f"Failed to reload {ext}: {e}")

    @commands.command(name="listcogs")
    @commands.is_owner()
    async def list_cogs(self, ctx):
        """List loaded cogs."""
        await ctx.send("Cogs loaded: " + ", ".join(self.bot.extensions.keys()))


async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCog(bot))
