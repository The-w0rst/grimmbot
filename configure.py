#!/usr/bin/env python3
"""Interactive configuration helper for the Goon Squad bots."""
from pathlib import Path
import logging

# Project repository: https://github.com/The-w0rst/grimmbot

TEMPLATE_PATH = Path("config/env_template.env")
SETUP_PATH = Path("config/setup.env")
VERSION = "1.4"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_existing(path: Path) -> dict:
    data = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip()
    return data


def main() -> None:
    logger.info("== Goon Squad Interactive Setup v%s ==\n", VERSION)
    TEMPLATE_PATH.parent.mkdir(parents=True, exist_ok=True)
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
    logger.info("\nSaved configuration to %s\n", SETUP_PATH)
    logger.info("Next steps:")
    logger.info("  1. Ensure Python 3.10+ is installed.")
    logger.info(
        "  2. Install dependencies: python -m pip install -r requirements/base.txt"
    )
    logger.info("  3. Run a bot, e.g.: python goon_bot.py\n")


if __name__ == "__main__":
    main()
