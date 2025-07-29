# flake8: noqa: E402
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from discord.ext import commands
import discord
from cogs.judge_cog import JudgeCog


def test_decide_vote_positive():
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)
    cog = JudgeCog(bot)
    vote = cog._decide_vote("I am sorry please help", "You are awful")
    assert vote == "User1"


def test_decide_vote_tie():
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)
    cog = JudgeCog(bot)
    vote = cog._decide_vote("Ok", "Okay")
    assert vote == "Both should compromise"
