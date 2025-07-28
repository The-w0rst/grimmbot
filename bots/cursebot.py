import discord
from discord.ext import commands

class CurseBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="?", intents=intents)
        self.add_command(self.curse)

    async def on_ready(self):
        print(f"CurseBot connected as {self.user}")

    @commands.command()
    async def curse(self, ctx: commands.Context):
        """Playfully scold the user."""
        await ctx.send(f"{ctx.author.mention}, you've been cursed!")
