"""Simple logging helper used across cogs and bot entrypoints."""

import logging
from logging.handlers import RotatingFileHandler


def setup_logging(log_file: str = "bot.log") -> None:
    """Configure the logging module to write timestamped messages."""
    handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=3)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[handler])


def log_message(text: str, level: int = logging.INFO) -> None:
    """Log a message at the given level."""
    logging.log(level, text)
