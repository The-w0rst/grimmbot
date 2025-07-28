from discord.ext import commands
import random

JOJO_DISPLAY_NAME = "JoJo"


class JojoCog(commands.Cog):
    """Send spontaneous loving messages to a friend."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.loving_lines = [
            "You are wonderful, Friend! 💖",
            "Hey JoJo, sending you big hugs!",
            "Friend, you light up this server!",
            "Just stopping by to say we adore you, JoJo!",
            "Stay amazing, Friend!"
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        if message.author.display_name == JOJO_DISPLAY_NAME and random.random() < 0.2:
            await message.channel.send(random.choice(self.loving_lines))

    @commands.command(name="jojo")
    async def jojo_cmd(self, ctx):
        """Send a random loving message to your friend."""
        await ctx.send(random.choice(self.loving_lines))


async def setup(bot: commands.Bot):
    await bot.add_cog(JojoCog(bot))
