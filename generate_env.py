#!/usr/bin/env python3
"""Create config/setup.env from current environment variables."""
from pathlib import Path
import os

TEMPLATE_PATH = Path("config/env_template.env")
OUTPUT_PATH = Path("config/setup.env")


def main() -> None:
    lines = []
    for line in TEMPLATE_PATH.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in line:
            lines.append(line)
            continue
        key = line.split("=", 1)[0]
        value = os.getenv(key, "")
        lines.append(f"{key}={value}")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
