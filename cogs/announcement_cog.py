import discord
from discord.ext import commands, tasks

COG_VERSION = "1.5"

# Server reference information for quick access
SERVER_ROLES = [
    "Server booster",
    "Goons",
    "Goonets",
    "Royalty",
]

SERVER_CATEGORIES = {
    "Intake": ["new-here"],
    "Gen pop": ["non-gooning", "gooning"],
    "Yapping": ["yapper's anonymous (voice)"],
    "Royalty": ["me-n-bea", "the-baby-yap (voice)"],
}


class AnnouncementCog(commands.Cog):
    """Send periodic announcements and list server layout. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.announcement_loop.start()

    @tasks.loop(hours=12)
    async def announcement_loop(self):
        guild = discord.utils.get(self.bot.guilds)
        if not guild:
            return
        channel = discord.utils.get(guild.text_channels, name="gooning")
        if channel:
            await channel.send(
                "Stay chaotic, Goons and Goonets! Check #non-gooning for chill chats."
            )

    @commands.command(name="serverinfo")
    async def server_info(self, ctx):
        """Display configured server roles and categories."""
        role_list = ", ".join(SERVER_ROLES)
        category_lines = [
            f"{cat}: {', '.join(chs)}" for cat, chs in SERVER_CATEGORIES.items()
        ]
        categories = "\n".join(category_lines)
        await ctx.send(f"**Roles**: {role_list}\n**Categories**:\n{categories}")


async def setup(bot: commands.Bot):
    await bot.add_cog(AnnouncementCog(bot))
