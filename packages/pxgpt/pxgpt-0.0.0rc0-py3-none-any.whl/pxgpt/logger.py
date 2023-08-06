from __future__ import annotations

import logging
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from logging import Logger


def get_logger(log_level: str) -> Logger:
    """Create or get the logger with the given configuration"""
    logger = logging.getLogger("pxgpt")
    logger.setLevel(log_level.upper())
    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(message)s"
    )

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
