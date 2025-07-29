import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

activity_logger = logging.getLogger("activity")
handler = RotatingFileHandler(LOG_DIR / "activity.log", maxBytes=1024 * 1024, backupCount=3)
formatter = logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
activity_logger.setLevel(logging.INFO)
activity_logger.addHandler(handler)


def log_action(action: str) -> None:
    activity_logger.info(action)
