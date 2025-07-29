import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.api_utils import ApiKeyCycle


def test_api_key_cycle_basic():
    cycle = ApiKeyCycle(["k1", "k2", "k3"])
    assert cycle.next() == "k1"
    assert cycle.next() == "k2"
    assert cycle.next() == "k3"
    # Should wrap around
    assert cycle.next() == "k1"


def test_api_key_cycle_empty():
    with pytest.raises(ValueError):
        ApiKeyCycle(["", None])
