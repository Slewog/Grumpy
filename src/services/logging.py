import json
import logging
import colorlog
import logging.config
from pathlib import Path

from src.utils import load_json_file

SETTING_FILE = "data/cfg/logs.json"
LOG_LEVELS = {
    logging.NOTSET: "NOTSET",
    logging.DEBUG: "DEBUG",
    logging.INFO: "INFO",
    logging.WARNING: "WARNING",
    logging.ERROR: "ERROR",
    logging.CRITICAL: "CRITICAL"
}

def get_log_level_name(logger: logging.Logger) -> str:
    current_level = logger.getEffectiveLevel()
    return LOG_LEVELS[current_level]


def build_logging(base_dir: Path) -> logging.Logger:
    json_file = base_dir / SETTING_FILE

    if not json_file.is_file():
        raise RuntimeError(f"Unable to access the settings files in {SETTING_FILE}, the program will shut down automatically.")

    config_dict = load_json_file(json_file)
    try:
        logging.config.dictConfig(config_dict)
    except ValueError as exc:
        raise RuntimeError(f"LOG SYSTEM ERROR: {exc}")

    logger = logging.getLogger("grumpy")
    log_level = get_log_level_name(logger)

    logger.info("The logging system has been successfully initialized.")
    logger.info("Log level - %s.", log_level)

    return logger
