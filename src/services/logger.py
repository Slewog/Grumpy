"""Logging formatter come from discord.py"""

import logging
from pathlib import Path

DATE_FMT = "%Y-%m-%d %H:%M:%S"
LOG_LEVELS = {
    logging.NOTSET: "NOTSET",
    logging.DEBUG: "DEBUG",
    logging.INFO: "INFO",
    logging.WARNING: "WARNING",
    logging.ERROR: "ERROR",
    logging.CRITICAL: "CRITICAL"
}


def get_log_level_name(current_level: int) -> str:
    return LOG_LEVELS[current_level]


class ColourFormatter(logging.Formatter):
    LEVEL_COLOURS = [
        (logging.DEBUG, "\x1b[40;1m"),
        (logging.INFO, "\x1b[34;1m"),
        (logging.WARNING, "\x1b[33;1m"),
        (logging.ERROR, "\x1b[31m"),
        (logging.CRITICAL, "\x1b[41m")
    ]

    FORMATS = {
        level: logging.Formatter(
            f"\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[32m%(name)s\x1b[0m\x1b[1m %(message)s",
            DATE_FMT,
        )
        for level, colour in LEVEL_COLOURS
    }

    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        # Override the traceback to always print in red.
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f"\x1b[31m{text}\x1b[0m"

        output = formatter.format(record)

        # Remove the cache layer.
        record.exc_text = None
        return output


def build_logger(base_dir: Path):
    """Build the bot logger and add FileHandler logging to discord."""
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(ColourFormatter())

    file_handler = logging.FileHandler(filename=base_dir / "data/logs/discord.log", encoding="utf-8", mode="w")
    file_handler.setFormatter(logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", DATE_FMT, style='{'))

    logger = logging.getLogger("grumpy")
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    discord = logging.getLogger("discord")
    discord.addHandler(file_handler)

    logger.info("The logging system has been successfully initialized.")

    return logger