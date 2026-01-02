import json
import logging
import logging.config
from pathlib import Path

SETTING_FILE = "logging_settings.json"
LEVELS = {
    logging.NOTSET: "NOTSET",
    logging.DEBUG: "DEBUG",
    logging.INFO: "INFO",
    logging.WARNING: "WARNING",
    logging.ERROR: "ERROR",
    logging.CRITICAL: "CRITICAL"
}


def build_logging(base_dir: Path):
    config_path = base_dir / "data" / SETTING_FILE
    config_dict = {}
    loaded = False

    try:
        with config_path.open("r", encoding="utf-8-sig") as config:
            logging.config.dictConfig(json.load(config))
        loaded = True
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to load log settings from from data/%s") from exc

    logging.config.dictConfig(config_dict)

    logger = logging.getLogger('grumpy.settings')
    log_lvl = LEVELS[logger.getEffectiveLevel()]

    if loaded:
        logger.info('Log settings loaded from data/%s', SETTING_FILE)
        logger.info("Log level - %s.", log_lvl)

    return log_lvl