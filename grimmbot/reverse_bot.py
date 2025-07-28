from .bot import Bot

class ReverseBot(Bot):
    """A bot that reverses the user's message."""
    def process(self, message: str) -> str:
        return message[::-1]
