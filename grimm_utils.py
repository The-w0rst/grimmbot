import random


LAMENTS = [
    "Another century, another pile of bones.",
    "I could go for a nice grave nap.",
    "Why does everyone assume I want to talk?",
    "Being undead is overrated.",
    "My scythe gets more respect than I do.",
]

INVENTORY_ITEMS = [
    "a cracked hourglass",
    "a chipped femur",
    "an old cloak clasp",
    "a tarnished coin",
    "a faded wanted poster",
    "a jar of suspicious dust",
    "a gloom-infused lantern",
    "a bundle of wilted roses",
    "a skull-shaped flask",
    "a bone polishing kit",
]


def gloom_level() -> int:
    """Return Grimm's current gloom level from 0 to 100."""
    return random.randint(0, 100)


def random_lament() -> str:
    """Return a random gloomy lament."""
    return random.choice(LAMENTS)


def random_item() -> str:
    """Return a random item from Grimm's stash."""
    return random.choice(INVENTORY_ITEMS)
