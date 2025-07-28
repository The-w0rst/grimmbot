import discord
from discord.ext import commands

class BloomBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="&", intents=intents)
        self.add_command(self.bloom)

    async def on_ready(self):
        print(f"BloomBot connected as {self.user}")

    @commands.command()
    async def bloom(self, ctx: commands.Context):
        """Send a cheerful message."""
        await ctx.send("BloomBot sends you positive vibes!")
