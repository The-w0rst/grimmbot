import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from discord.ext import commands
import discord

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

error_logger = logging.getLogger("bot_errors")
handler = RotatingFileHandler(LOG_DIR / "errors.log", maxBytes=1024 * 1024, backupCount=3)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
error_logger.setLevel(logging.ERROR)
error_logger.addHandler(handler)


def setup_error_handlers(bot: commands.Bot, admin_id: int | None = None) -> None:
    async def notify_admin(msg: str) -> None:
        if not admin_id:
            return
        user = bot.get_user(admin_id)
        if user:
            try:
                await user.send(msg)
            except discord.HTTPException:
                pass

    @bot.event
    async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Slow down! Try again in {round(error.retry_after, 1)}s.")
            return
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You lack permission to run that command.")
            return
        await ctx.send("Something went wrong. The incident has been logged.")
        error_logger.exception("Command error in %s: %s", ctx.command, error)
        await notify_admin(f"Command error in {ctx.command}: {error}")

    @bot.event
    async def on_error(event: str, *args, **kwargs) -> None:
        error_logger.exception("Unhandled exception in event %s", event, exc_info=True)
        await notify_admin(f"Critical error in event {event}. Check logs.")
