"""Collection of Grimmbot cogs with version tracking."""

from pathlib import Path

PACKAGE_VERSION = "1.6"
__all__ = [p.stem for p in Path(__file__).parent.glob("*_cog.py")]
