import logging
import os
from logging import Logger

def setup_logging(level: str | int | None = None) -> None:
    lvl = level or os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(
        level=lvl,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

def get_logger(name: str) -> Logger:
    return logging.getLogger(name)
