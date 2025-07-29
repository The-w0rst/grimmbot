#!/usr/bin/env python3
"""Interactive installer for the Goon Squad bots.

This version speaks in Curse's voice and guides the user through filling
in every token one by one with friendly descriptions. A few validation
checks help guard against missing values."""
import sys
import logging
from src.logger import setup_logging, log_message
from colorama import Fore, Style, init

# Project repository: https://github.com/The-w0rst/grimmbot
import subprocess
from pathlib import Path
import shutil
from config.settings import validate_template

setup_logging("install.log")
logger = logging.getLogger(__name__)
init(autoreset=True)
CYAN = Fore.CYAN + Style.BRIGHT
GREEN = Fore.GREEN + Style.BRIGHT
YELLOW = Fore.YELLOW + Style.BRIGHT
RED = Fore.RED + Style.BRIGHT
RESET = Style.RESET_ALL

VERSION = "1.5"

TEMPLATE_PATH = Path("config/env_template.env")
SETUP_PATH = Path("config/setup.env")

# Environment variables that must not be left blank. Leaving these empty will
# likely prevent a bot from starting correctly.
REQUIRED_VARS = {
    "GRIMM_DISCORD_TOKEN",
    "BLOOM_DISCORD_TOKEN",
    "CURSE_DISCORD_TOKEN",
    "DISCORD_TOKEN",
}


def read_existing(path: Path) -> dict:
    data = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip()
    return data


def validate_env(path: Path) -> list:
    """Return a list of required variables that are missing values."""
    data = read_existing(path)
    missing = [var for var in REQUIRED_VARS if not data.get(var)]
    return missing


def check_python() -> None:
    logger.info(CYAN + "Step 1/4: Checking Python version..." + RESET)
    if sys.version_info < (3, 10):
        sys.exit("Python 3.10 or newer is required. Aborting.")
    logger.info(GREEN + "\u2714 Python %s.%s detected\n" + RESET, sys.version_info.major, sys.version_info.minor)


def install_requirements() -> None:
    logger.info(CYAN + "Step 2/4: Installing dependencies from requirements/base.txt" + RESET)
    choice = input(YELLOW + "Install dependencies now? [Y/n] " + RESET).strip().lower()
    if choice in ("", "y", "yes"):
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements/base.txt"]
        )
    logger.info("")


def configure_env() -> None:
    logger.info(CYAN + "Step 3/4: Time to hand over the keys. I'm Curse and I'll keep them safe!" + RESET)
    TEMPLATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not SETUP_PATH.exists():
        shutil.copyfile(TEMPLATE_PATH, SETUP_PATH)
    existing = read_existing(SETUP_PATH)
    lines = []
    friendly = {
        "GRIMM_DISCORD_TOKEN": "Grimm's Discord token",
        "GRIMM_API_KEY_1": "Grimm API key #1",
        "GRIMM_API_KEY_2": "Grimm API key #2",
        "GRIMM_API_KEY_3": "Grimm API key #3",
        "SOCKET_SERVER_URL": "(optional) Socket.IO status URL",
        "BLOOM_DISCORD_TOKEN": "Bloom's Discord token",
        "BLOOM_API_KEY_1": "Bloom API key #1",
        "BLOOM_API_KEY_2": "Bloom API key #2",
        "BLOOM_API_KEY_3": "Bloom API key #3",
        "CURSE_DISCORD_TOKEN": "Curse's Discord token",
        "CURSE_API_KEY_1": "Curse API key #1",
        "CURSE_API_KEY_2": "Curse API key #2",
        "CURSE_API_KEY_3": "Curse API key #3",
        "DISCORD_TOKEN": "Unified bot token",
        "OPENAI_API_KEY": "OpenAI API key",
    }
    for line in TEMPLATE_PATH.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in line:
            lines.append(line)
            continue
        key = line.split("=", 1)[0]
        desc = friendly.get(key, key)
        default = existing.get(key, "")
        prompt = (f"{desc} [{default}]: " if default else f"{desc}: ")
        prompt = YELLOW + prompt + RESET
        while True:
            try:
                value = input(prompt).strip() or default
            except KeyboardInterrupt:
                logger.info(RED + "\nAborted." + RESET)
                sys.exit(1)
            if key in REQUIRED_VARS and not value:
                logger.info(RED + "This value is required." + RESET)
                continue
            break
        lines.append(f"{key}={value}")
    SETUP_PATH.write_text("\n".join(lines) + "\n")
    logger.info(GREEN + "\nSaved configuration to %s\n" + RESET, SETUP_PATH)
    missing = validate_env(SETUP_PATH)
    if missing:
        logger.warning(RED + "Warning: the following values are still blank: %s" + RESET, ", ".join(missing))
    missing_keys = validate_template()
    if missing_keys:
        logger.warning(
            RED + "Warning: these variables are defined in the template but missing from setup.env: %s" + RESET,
            ", ".join(missing_keys),
        )


def choose_bot() -> None:
    logger.info(CYAN + "Step 4/4: Installation finished!" + RESET)
    options = {
        "1": ("GrimmBot", "grimm_bot.py"),
        "2": ("BloomBot", "bloom_bot.py"),
        "3": ("CurseBot", "curse_bot.py"),
        "4": ("GoonBot (all cogs)", "goon_bot.py"),
        "5": ("All bots", None),
        "0": ("Exit", None),
    }
    for key, (name, _) in options.items():
        logger.info(" %s. %s", key, name)
    try:
        choice = input(YELLOW + "Run a bot now? [0-5] " + RESET).strip()
    except KeyboardInterrupt:
        logger.info(RED + "\nAborted." + RESET)
        sys.exit(1)

    if choice == "5":
        scripts = ["grimm_bot.py", "bloom_bot.py", "curse_bot.py", "goon_bot.py"]
        processes = [subprocess.Popen([sys.executable, s]) for s in scripts]
        try:
            for p in processes:
                p.wait()
        except KeyboardInterrupt:
            logger.info(RED + "\nStopping bots…" + RESET)
            for p in processes:
                p.terminate()
            for p in processes:
                p.wait()
    else:
        script = options.get(choice, (None, None))[1]
        if script:
            subprocess.call([sys.executable, script])
        else:
            logger.info(
                "You can start a bot later using one of the python commands above."
            )


def main() -> None:
    logger.info(CYAN + "== Goon Squad Bot Installer v%s ==" + RESET, VERSION)
    log_message("Installer starting")
    logger.info("Curse here. I'll walk you through this. Let's do it!\n")
    try:
        check_python()
        install_requirements()
        configure_env()
        choose_bot()
    except KeyboardInterrupt:
        logger.info(RED + "\nInstaller aborted." + RESET)
        sys.exit(1)
    logger.info(
        GREEN + "Congratulations. Your discord server is now cursed! That wasn't very smart of you…" + RESET
    )


if __name__ == "__main__":
    main()
