"""Simple logging helper used across cogs and bot entrypoints."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

try:
    from colorama import Fore, Style, init as colorama_init
except Exception:  # pragma: no cover - colorama optional for tests
    Fore = Style = None

    def colorama_init(*_args, **_kwargs):
        return


def setup_logging(log_file: str = "bot.log") -> None:
    """Configure logging with file and colorized console handlers."""
    colorama_init(autoreset=True)

    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)
    file_handler = RotatingFileHandler(log_path / log_file, maxBytes=1024 * 1024, backupCount=3)
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    if Fore and Style:

        class ColorFormatter(logging.Formatter):
            COLORS = {
                logging.DEBUG: Fore.CYAN,
                logging.INFO: Fore.GREEN,
                logging.WARNING: Fore.YELLOW,
                logging.ERROR: Fore.RED,
                logging.CRITICAL: Fore.MAGENTA,
            }

            def format(
                self, record: logging.LogRecord
            ) -> str:  # pragma: no cover - visual only
                color = self.COLORS.get(record.levelno, "")
                message = super().format(record)
                return f"{color}{message}{Style.RESET_ALL}"

        console_formatter = ColorFormatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%H:%M:%S"
        )
    else:  # pragma: no cover - fallback for tests
        console_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        )
    console_handler.setFormatter(console_formatter)

    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])


def log_message(text: str, level: int = logging.INFO) -> None:
    """Log a message at the given level."""
    logging.log(level, text)
