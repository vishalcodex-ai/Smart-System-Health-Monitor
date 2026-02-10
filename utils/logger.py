# ==========================================
# File: logger.py
# Project: Smart System Health Monitor
# Description:
#   Central logging utility for the entire
#   project. Provides consistent logging
#   format, log levels, console & file
#   handlers with rotation support.
# ==========================================

import logging
import os
from logging.handlers import RotatingFileHandler

from config.settings import (
    LOG_LEVEL,
    LOG_TO_FILE,
    LOG_TO_CONSOLE,
    LOG_FILE_PATH
)

# -------------------------------
# Logger Cache
# -------------------------------
_LOGGER_CACHE = {}

# -------------------------------
# Log Level Mapping
# -------------------------------
LOG_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

# -------------------------------
# Get Logger Function
# -------------------------------
def get_logger(name):
    """
    Get or create a logger with the given name.

    Args:
        name (str): Logger name (usually __name__)

    Returns:
        logging.Logger
    """

    if name in _LOGGER_CACHE:
        return _LOGGER_CACHE[name]

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL_MAP.get(LOG_LEVEL, logging.INFO))
    logger.propagate = False

    # ---------------------------
    # Log Format
    # ---------------------------
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ---------------------------
    # Console Handler
    # ---------------------------
    if LOG_TO_CONSOLE:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVEL_MAP.get(LOG_LEVEL, logging.INFO))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # ---------------------------
    # File Handler with Rotation
    # ---------------------------
    if LOG_TO_FILE:
        log_dir = os.path.dirname(LOG_FILE_PATH)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = RotatingFileHandler(
            LOG_FILE_PATH,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(LOG_LEVEL_MAP.get(LOG_LEVEL, logging.INFO))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    _LOGGER_CACHE[name] = logger
    return logger

# -------------------------------
# End of logger.py
# -------------------------------
