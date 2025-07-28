import random

class Bot3:
    """A simple joke bot."""
    JOKES = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I told my computer I needed a break, and it said 'No problem: I'll go to sleep.'",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
    ]

    def tell_joke(self) -> str:
        return random.choice(self.JOKES)

def run():
    print(Bot3().tell_joke())

if __name__ == '__main__':
    run()
