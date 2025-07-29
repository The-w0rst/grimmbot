# flake8: noqa
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from discord.ext import commands
import discord
from cogs.fun_cog import FunCog


class DummyCtx:
    def __init__(self):
        self.sent = []

    async def send(self, message):
        self.sent.append(message)


@pytest.mark.asyncio
async def test_roll_invalid():
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)
    cog = FunCog(bot)
    ctx = DummyCtx()
    await cog.roll.callback(cog, ctx, sides=1)
    assert ctx.sent == ["Dice need at least 2 sides!"]
