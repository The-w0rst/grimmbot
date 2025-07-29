HEALTH_STATS = {
    "Grimm": 100,
    "Bloom": 100,
    "Curse": 100,
}


def get_health(bot: str) -> int:
    return HEALTH_STATS.get(bot, 100)


def set_health(bot: str, value: int) -> None:
    HEALTH_STATS[bot] = max(0, min(100, value))


def get_menu() -> str:
    lines = ["**Bot Health**"]
    for name, hp in HEALTH_STATS.items():
        lines.append(f"{name}: {hp}/100")
    return "\n".join(lines)
