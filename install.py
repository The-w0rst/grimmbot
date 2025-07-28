#!/usr/bin/env python3
"""Interactive installer for the Goon Squad bots."""
import sys
# Project repository: https://github.com/The-w0rst/grimmbot
import subprocess
from pathlib import Path
import shutil

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
    if sys.version_info < (3, 8):
        sys.exit("Python 3.8 or newer is required. Aborting.")
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
    print("Step 3/4: Setting up configuration file")
    TEMPLATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not SETUP_PATH.exists():
        shutil.copyfile(TEMPLATE_PATH, SETUP_PATH)
    existing = read_existing(SETUP_PATH)
    lines = []
    for line in TEMPLATE_PATH.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in line:
            lines.append(line)
            continue
        key = line.split("=", 1)[0]
        default = existing.get(key, "")
        prompt = f"{key} [{default}]: " if default else f"{key}: "
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


def main() -> None:
    print("== Goon Squad Bot Installer ==\n")
    check_python()
    install_requirements()
    configure_env()
    choose_bot()


if __name__ == "__main__":
    main()
