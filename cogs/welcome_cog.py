import discord
from discord.ext import commands

COG_VERSION = "1.4"

WELCOME_LINES = {
    "Grimm": "Another soul joins us... Welcome, {member}.",
    "Bloom": "Yay! {member}, you're finally here! \U0001f389",
    "Curse": "Heh, {member} stumbled into our lair.",
    "default": "Welcome {member}!",
}

GOODBYE_LINES = {
    "Grimm": "Farewell, {member}. Don't get lost out there.",
    "Bloom": "Aww, {member} left the party. Come back soon!",
    "Curse": "Bye-bye {member}, thanks for the chaos.",
    "default": "Goodbye {member}.",
}


class WelcomeCog(commands.Cog):
    """Send welcome and goodbye messages and auto-assign roles. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _line(self, name: str, member: discord.Member, table: dict[str, str]) -> str:
        template = table.get(name, table["default"])
        return template.format(
            member=member.mention if "welcome" in template else member.display_name
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        role = discord.utils.get(guild.roles, name="Member")
        if role:
            await member.add_roles(role)
        channel = (
            discord.utils.get(guild.text_channels, name="general")
            or guild.text_channels[0]
        )
        line = self._line(
            self.bot.user.name if self.bot.user else "default", member, WELCOME_LINES
        )
        await channel.send(line)
        try:
            await member.send(line)
        except discord.Forbidden:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        guild = member.guild
        channel = (
            discord.utils.get(guild.text_channels, name="general")
            or guild.text_channels[0]
        )
        line = self._line(
            self.bot.user.name if self.bot.user else "default", member, GOODBYE_LINES
        )
        await channel.send(line)


async def setup(bot: commands.Bot):
    await bot.add_cog(WelcomeCog(bot))
