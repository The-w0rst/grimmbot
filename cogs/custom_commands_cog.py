import json
from pathlib import Path
import discord
from discord.ext import commands

COG_VERSION = "1.0"

COMMANDS_PATH = Path("config/custom_commands.json")


def load_commands() -> dict:
    if COMMANDS_PATH.exists():
        try:
            return json.loads(COMMANDS_PATH.read_text())
        except Exception:
            return {}
    return {}


def save_commands(data: dict) -> None:
    COMMANDS_PATH.write_text(json.dumps(data, indent=2))


class CustomCommandsCog(commands.Cog):
    """Admin defined simple commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.commands_map = load_commands()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def addcmd(self, ctx, name: str, *, response: str):
        """Add a custom command."""
        self.commands_map[name.lower()] = response
        save_commands(self.commands_map)
        await ctx.send(f"Added custom command `{name}`.")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def delcmd(self, ctx, name: str):
        """Delete a custom command."""
        if name.lower() in self.commands_map:
            del self.commands_map[name.lower()]
            save_commands(self.commands_map)
            await ctx.send(f"Deleted `{name}`.")
        else:
            await ctx.send("No such command.")

    @commands.command()
    async def listcmds(self, ctx):
        """List all custom commands."""
        if self.commands_map:
            await ctx.send(", ".join(sorted(self.commands_map.keys())))
        else:
            await ctx.send("No custom commands set.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return
        name = message.content.strip().lower()
        if name in self.commands_map:
            await message.channel.send(self.commands_map[name])


async def setup(bot: commands.Bot):
    await bot.add_cog(CustomCommandsCog(bot))
