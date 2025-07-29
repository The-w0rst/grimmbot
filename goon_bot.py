# Project repository: https://github.com/The-w0rst/grimmbot
import asyncio
import os
import glob
import logging
import subprocess
import sys
import discord
from discord.ext import commands
from pathlib import Path
import datetime
from config.settings import load_config
from src.logger import setup_logging, log_message
from src.error_handler import setup_error_handlers

setup_logging("goon_bot.log")
logger = logging.getLogger(__name__)
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0")) or None

# Track subprocesses for the individual bots
child_processes = []


def launch_other_bots() -> None:
    """Launch Grimm, Bloom, and Curse bots as subprocesses."""
    scripts = ["grimm_bot.py", "bloom_bot.py", "curse_bot.py"]
    for script in scripts:
        path = Path(__file__).resolve().parent / script
        if not path.exists():
            logger.warning("%s missing", script)
            continue
        try:
            proc = subprocess.Popen([sys.executable, str(path)])
            child_processes.append(proc)
            logger.info("Launched %s (PID %s)", script, proc.pid)
        except Exception as exc:
            logger.warning("Failed to launch %s: %s", script, exc)


# Load a single shared configuration file for all bots
ENV_PATH = Path(__file__).resolve().parent / "config" / "setup.env"
if not ENV_PATH.exists():
    raise SystemExit("config/setup.env missing. Run 'python install.py' first.")
load_config({"DISCORD_TOKEN"})
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


def check_required() -> None:
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN missing")
        raise SystemExit(1)


# Allow '!', '*', and '?' prefixes like the individual bots


async def get_prefix(bot, message):
    prefixes = ["!", "*", "?"]
    return commands.when_mentioned_or(*prefixes)(bot, message)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)
setup_error_handlers(bot, ADMIN_USER_ID)
START_TIME = datetime.datetime.utcnow()


@bot.event
async def on_ready():
    check_required()
    guilds = ", ".join(g.name for g in bot.guilds)
    cogs = ", ".join(bot.cogs.keys())
    env = {"DISCORD_TOKEN": (DISCORD_TOKEN[:4] + "...") if DISCORD_TOKEN else "missing"}
    logger.info("Goon online | guilds: %s | cogs: %s | env: %s", guilds, cogs, env)
    log_message("Goon bot ready")


@bot.event
async def on_command_error(ctx, error):
    logger.exception("Command error: %s", error)
    await ctx.send("Command failed. Check logs.")


@bot.command(name="health")
async def health(ctx):
    """Report bot health statistics."""
    try:
        uptime = datetime.datetime.utcnow() - START_TIME
        latency = round(bot.latency * 1000)
        msg = (
            f"Uptime: {uptime}\n"
            f"Ping: {latency} ms\n"
            f"Cogs: {len(bot.cogs)} loaded"
        )
        await ctx.send(msg)
    except Exception as exc:
        logger.exception("health command failed: %s", exc)


async def load_startup_cogs():
    for file in glob.glob("cogs/*_cog.py"):
        ext = f"cogs.{os.path.splitext(os.path.basename(file))[0]}"
        try:
            await bot.load_extension(ext)
            logger.info("Loaded %s", ext)
        except Exception as e:
            logger.warning("Failed to load %s: %s", ext, e)


asyncio.run(load_startup_cogs())
launch_other_bots()
check_required()
try:
    bot.run(DISCORD_TOKEN)
finally:
    for proc in child_processes:
        try:
            proc.terminate()
        except Exception:
            pass
    log_message("Goon shutting down")
