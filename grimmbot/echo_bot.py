from .bot import Bot

class EchoBot(Bot):
    """A bot that echoes the user's message."""
    def process(self, message: str) -> str:
        return message
