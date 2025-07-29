#!/usr/bin/env python3
"""Diagnostic checks for Goon Squad Discord bots."""

from __future__ import annotations

import logging
import os
import sys
import importlib.util
from importlib import metadata
from pathlib import Path

from dotenv import load_dotenv
from src.logger import setup_logging
from colorama import Fore, Style, init

REQUIRED_ENV_VARS = [
    "GRIMM_DISCORD_TOKEN",
    "BLOOM_DISCORD_TOKEN",
    "CURSE_DISCORD_TOKEN",
    "GRIMM_API_KEY_1",
    "BLOOM_API_KEY_1",
    "CURSE_API_KEY_1",
]

REQUIRED_FILES = [
    ".env",
    "requirements/base.txt",
    "grimm_bot.py",
    "bloom_bot.py",
    "curse_bot.py",
    "goon_bot.py",
]

REQUIRED_PACKAGES = [
    "discord",
    "openai",
    "dotenv",
]

BASE_PATH = Path(__file__).resolve().parent

logger = logging.getLogger(__name__)


def check_env_file() -> bool:
    env = BASE_PATH / ".env"
    logger.info("Checking for .env file…")
    if not env.exists():
        logger.error(".env file not found at %s", env)
        return False
    load_dotenv(env)
    logger.info("Found .env file")
    return True


def check_required_env_vars() -> list[str]:
    logger.info("Checking required environment variables…")
    missing = [var for var in REQUIRED_ENV_VARS if os.getenv(var) is None]
    if missing:
        logger.error("Missing required .env variables: %s", ", ".join(missing))
    else:
        logger.info("All required .env variables are set")
    return missing


def check_required_files() -> list[str]:
    logger.info("Checking required files…")
    missing: list[str] = []
    for name in REQUIRED_FILES:
        if not (BASE_PATH / name).exists():
            missing.append(name)
    if missing:
        logger.error("Missing files: %s", ", ".join(missing))
    else:
        logger.info("All required files are present")
    return missing


def check_required_packages() -> list[str]:
    logger.info("Checking required packages…")
    missing: list[str] = []
    for pkg in REQUIRED_PACKAGES:
        if importlib.util.find_spec(pkg) is None:
            missing.append(pkg)
            continue
        try:
            version = metadata.version(pkg)
            logger.info("%s version %s", pkg, version)
        except metadata.PackageNotFoundError:
            logger.info("%s installed", pkg)
    if missing:
        logger.error("Missing Python packages: %s", ", ".join(missing))
    else:
        logger.info("All required packages are installed")
    return missing


def check_python_version() -> bool:
    logger.info("Checking Python version…")
    if sys.version_info < (3, 9):
        logger.error("Python 3.9 or later is required")
        return False
    logger.info("Python version OK: %s", sys.version.split()[0])
    return True


def check_for_hardcoded_secrets() -> list[str]:
    logger.info("Scanning for hardcoded secrets…")
    issues: list[str] = []
    for path in BASE_PATH.rglob("*.py"):
        for line_no, line in enumerate(path.read_text().splitlines(), 1):
            if "discord" in line.lower() and "token" in line.lower() and "os.getenv" not in line:
                issues.append(f"{path}:{line_no}")
            if "sk-" in line and "os.getenv" not in line:
                issues.append(f"{path}:{line_no}")
    if issues:
        logger.warning("Potential secrets found: %s", ", ".join(issues))
    else:
        logger.info("No hardcoded secrets detected")
    return issues


def main() -> None:
    setup_logging("diagnostics.log")
    init(autoreset=True)
    logger.info(Fore.CYAN + "==== Goon Squad Bot Diagnostics ====" + Style.RESET_ALL)
    errors = 0
    if not check_env_file():
        errors += 1
    errors += len(check_required_env_vars())
    errors += len(check_required_files())
    errors += len(check_required_packages())
    errors += len(check_for_hardcoded_secrets())
    if not check_python_version():
        errors += 1
    if errors == 0:
        logger.info(Fore.GREEN + "All checks passed! You should be able to start your bots." + Style.RESET_ALL)
    else:
        logger.error(
            Fore.RED + f"{errors} issues found. Please resolve before running your bots." + Style.RESET_ALL
        )
        sys.exit(1)
    logger.info(Fore.CYAN + "====================================" + Style.RESET_ALL)


if __name__ == "__main__":
    main()
