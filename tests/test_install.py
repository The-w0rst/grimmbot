# flake8: noqa: E402
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from install import read_existing, validate_env


def test_read_existing(tmp_path):
    env = tmp_path / "sample.env"
    env.write_text("A=1\nB=2\n#C=3\n")
    assert read_existing(env) == {"A": "1", "B": "2"}


def test_validate_env(tmp_path):
    content = """GRIMM_DISCORD_TOKEN=123
BLOOM_DISCORD_TOKEN=
CURSE_DISCORD_TOKEN=abc
DISCORD_TOKEN=
"""
    env = tmp_path / "vars.env"
    env.write_text(content)
    missing = validate_env(env)
    assert set(missing) == {"BLOOM_DISCORD_TOKEN", "DISCORD_TOKEN"}
