from __future__ import annotations

"""Shared configuration loader for Goon Squad bots."""

import os
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent / "setup.env"
TEMPLATE_PATH = Path(__file__).resolve().parent / "env_template.env"

REQUIRED_VARS = {
    "GRIMM_DISCORD_TOKEN",
    "BLOOM_DISCORD_TOKEN",
    "CURSE_DISCORD_TOKEN",
    "DISCORD_TOKEN",
}


def load_config(required: set[str] | None = None) -> dict:
    """Load environment variables and optionally validate required keys."""
    if not ENV_PATH.exists():
        raise RuntimeError(
            "config/setup.env missing. Run 'python install.py' first."
        )
    load_dotenv(ENV_PATH)
    required = set(required or [])
    missing = [var for var in required if not os.getenv(var)]
    if missing:
        raise RuntimeError(
            "Missing required environment variables: " + ", ".join(missing)
        )
    return {key: os.getenv(key) for key in os.environ.keys()}


def validate_template() -> list[str]:
    """Return a list of variables in the template that are missing in setup.env."""
    def parse_vars(path: Path) -> set[str]:
        vars_set = set()
        for line in path.read_text().splitlines():
            if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
                continue
            vars_set.add(line.split("=", 1)[0].strip())
        return vars_set

    template_vars = parse_vars(TEMPLATE_PATH)
    setup_vars = parse_vars(ENV_PATH) if ENV_PATH.exists() else set()
    return sorted(template_vars - setup_vars)
