from itertools import cycle
from typing import Iterable


class ApiKeyCycle:
    """Cycle through multiple API keys to spread usage."""

    def __init__(self, keys: Iterable[str]):
        clean_keys = [k for k in keys if k]
        if not clean_keys:
            raise ValueError("No API keys provided")
        self._cycle = cycle(clean_keys)

    def next(self) -> str:
        return next(self._cycle)
