from typing import List

from .bot import Bot

class Coordinator:
    """Coordinate multiple bots to process messages sequentially."""
    def __init__(self, bots: List[Bot]):
        self.bots = bots

    def process(self, message: str) -> str:
        """Pass the message through all bots in sequence."""
        for bot in self.bots:
            message = bot.process(message)
        return message
