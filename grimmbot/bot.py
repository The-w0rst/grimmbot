class Bot:
    """Base bot class."""
    def process(self, message: str) -> str:
        """Process a message and return the response."""
        raise NotImplementedError("Bots must implement process()")
