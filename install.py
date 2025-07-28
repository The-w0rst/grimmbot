#!/usr/bin/env python3
"""Interactive installer for the Goon Squad bots.

This version speaks in Curse's voice and guides the user through filling
in every token one by one with friendly descriptions."""
import sys

# Project repository: https://github.com/The-w0rst/grimmbot
import subprocess
from pathlib import Path
import shutil

VERSION = "1.3"

TEMPLATE_PATH = Path("config/env_template.env")
SETUP_PATH = Path("config/setup.env")


def read_existing(path: Path) -> dict:
    data = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip()
    return data


def check_python() -> None:
    print("Step 1/4: Checking Python version...")
    if sys.version_info < (3, 10):
        sys.exit("Python 3.10 or newer is required. Aborting.")
    print(f"✔ Python {sys.version_info.major}.{sys.version_info.minor} detected.\n")


def install_requirements() -> None:
    print("Step 2/4: Installing dependencies from requirements/base.txt")
    choice = input("Install dependencies now? [Y/n] ").strip().lower()
    if choice in ("", "y", "yes"):
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements/base.txt"]
        )
    print()


def configure_env() -> None:
    print("Step 3/4: Time to hand over the keys. I'm Curse and I'll keep them safe!")
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
        prompt = f"{desc} [{default}]: " if default else f"{desc}: "
        value = input(prompt).strip() or default
        lines.append(f"{key}={value}")
    SETUP_PATH.write_text("\n".join(lines) + "\n")
    print(f"\nSaved configuration to {SETUP_PATH}\n")


def choose_bot() -> None:
    print("Step 4/4: Installation finished!")
    options = {
        "1": ("GrimmBot", "grimm_bot.py"),
        "2": ("BloomBot", "bloom_bot.py"),
        "3": ("CurseBot", "curse_bot.py"),
        "4": ("GoonBot (all cogs)", "goon_bot.py"),
        "0": ("Exit", None),
    }
    for key, (name, _) in options.items():
        print(f" {key}. {name}")
    choice = input("Run a bot now? [0-4] ").strip()
    script = options.get(choice, (None, None))[1]
    if script:
        subprocess.call([sys.executable, script])
    else:
        print("You can start a bot later using one of the python commands above.")


def main() -> None:
    print(f"== Goon Squad Bot Installer v{VERSION} ==")
    print("Curse here. I'll walk you through this. Let's do it!\n")
    check_python()
    install_requirements()
    configure_env()
    choose_bot()


if __name__ == "__main__":
    main()
