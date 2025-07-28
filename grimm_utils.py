import random


LAMENTS = [
    "Another century, another pile of bones.",
    "I could go for a nice grave nap.",
    "Why does everyone assume I want to talk?",
    "Being undead is overrated.",
    "My scythe gets more respect than I do.",
    "I miss the quiet of the crypt.",
    "These bones ache in ways you wouldn't believe.",
    "Immortality comes with endless paperwork.",
    "Is it too much to ask for some eternal rest?",
    "Even my shadows are tired of me.",
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
    "a jar of grave dirt",
    "a cracked monocle",
    "a pocket full of spider webs",
    "a rusted lock with no key",
    "a map to nowhere",
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
