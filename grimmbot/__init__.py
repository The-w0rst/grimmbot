"""Grimmbot package with simple example bots."""

from .bot import Bot
from .echo_bot import EchoBot
from .reverse_bot import ReverseBot
from .uppercase_bot import UppercaseBot
from .coordinator import Coordinator

__all__ = [
    'Bot',
    'EchoBot',
    'ReverseBot',
    'UppercaseBot',
    'Coordinator',
]
