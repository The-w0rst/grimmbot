import discord
from discord.ext import commands

class GrimBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.add_command(self.hello)

    async def on_ready(self):
        print(f"GrimBot connected as {self.user}")

    @commands.command()
    async def hello(self, ctx: commands.Context):
        """Respond with a friendly greeting."""
        await ctx.send("Greetings from GrimBot!")
