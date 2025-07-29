# flake8: noqa
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import settings


def test_validate_template(monkeypatch, tmp_path):
    template = tmp_path / "template.env"
    setup = tmp_path / "setup.env"
    template.write_text("A=\nB=\n")
    setup.write_text("A=1\n")
    monkeypatch.setattr(settings, "TEMPLATE_PATH", template)
    monkeypatch.setattr(settings, "ENV_PATH", setup)
    missing = settings.validate_template()
    assert missing == ["B"]
