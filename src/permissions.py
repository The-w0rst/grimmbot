import json
from pathlib import Path
from typing import Callable
from discord.ext import commands
import logging

CONFIG_PATH = Path("config/command_config.json")
logger = logging.getLogger(__name__)


def _load() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except Exception as exc:  # pragma: no cover - invalid json
            logger.warning("Failed to read %s: %s", CONFIG_PATH, exc)
    return {}


_CONFIG = _load()


def command_settings(name: str) -> dict:
    return _CONFIG.get(name, {})


def permission_check(name: str) -> Callable:
    settings = command_settings(name)
    allowed_roles = {r.lower() for r in settings.get("roles", [])}
    allowed_users = {int(u) for u in settings.get("users", []) if str(u).isdigit()}

    async def predicate(ctx: commands.Context) -> bool:
        if allowed_users and ctx.author.id in allowed_users:
            return True
        if allowed_roles and any(r.name.lower() in allowed_roles for r in ctx.author.roles):
            return True
        if not allowed_roles and not allowed_users:
            return True
        raise commands.MissingPermissions(["role"])

    return commands.check(predicate)


def apply_cooldown(name: str) -> Callable:
    seconds = command_settings(name).get("cooldown")
    if seconds:
        return commands.cooldown(1, int(seconds), commands.BucketType.user)

    def wrapper(func: Callable) -> Callable:
        return func

    return wrapper
