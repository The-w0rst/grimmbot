from .bot import Bot

class UppercaseBot(Bot):
    """A bot that converts messages to uppercase."""
    def process(self, message: str) -> str:
        return message.upper()
