from discord.ext import commands

COG_VERSION = "1.3"

# Short help messages for each bot so they can be reused in other commands
GRIMM_HELP = (
    "**GrimmBot** (`!` prefix) - the cranky skeleton.\n"
    "Try commands like `!protectbloom`, `!gloom`, `!roast` and `!bonk`."
)

BLOOM_HELP = (
    "**BloomBot** (`*` prefix) - bubbly chaos.\n"
    "Try `*hug`, `*sing`, `*sparkle`, `*play <url>` and more."
)

CURSE_HELP = (
    "**CurseBot** (`?` prefix) - the mischievous cat.\n"
    "Try `?insult`, `?scratch @user`, `?pounce` or `?curse_me`."
)


class HelpCog(commands.Cog):
    """Provide help commands for the goons. Version 1.3."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="grimmhelp")
    async def grimm_help(self, ctx: commands.Context):
        """Show help for GrimmBot."""
        await ctx.send(GRIMM_HELP)

    @commands.command(name="bloomhelp")
    async def bloom_help(self, ctx: commands.Context):
        """Show help for BloomBot."""
        await ctx.send(BLOOM_HELP)

    @commands.command(name="cursehelp")
    async def curse_help(self, ctx: commands.Context):
        """Show help for CurseBot."""
        await ctx.send(CURSE_HELP)

    @commands.command(name="helpall")
    async def help_all(self, ctx: commands.Context):
        """Show help for all bots at once."""
        for msg in (GRIMM_HELP, BLOOM_HELP, CURSE_HELP):
            await ctx.send(msg)


async def setup(bot: commands.Bot):
    """Load the cog."""
    await bot.add_cog(HelpCog(bot))
