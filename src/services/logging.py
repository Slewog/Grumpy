import json
import logging
import logging.config
from pathlib import Path

logging.DEBUG
SETTING_FILE = "logging_settings.json"

def get_log_level(effective_level: int) -> str:
    level = 'None'

    if effective_level == logging.NOTSET:
        level = "NOTSET"
    elif effective_level == logging.DEBUG:
        level = "DEBUG"
    elif effective_level == logging.INFO:
        level = "INFO"
    elif effective_level == logging.WARNING:
        level = "WARNING"
    elif effective_level == logging.ERROR:
        level = "ERROR"
    elif effective_level == logging.CRITICAL:
        level = "CRITICAL"

    return level

def build_logging(base_dir: Path):
    settings_path = base_dir / "data" / SETTING_FILE
    config_dict = {}
    loaded = False

    try:
        with settings_path.open("r", encoding="utf-8-sig") as fp:
            config_dict = json.load(fp)
            loaded = True
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to load log settings from from data/%s") from exc

    logging.config.dictConfig(config_dict)

    logger = logging.getLogger('BOT')
    log_lvl = get_log_level(logger.getEffectiveLevel())

    if loaded:
        logger.info('Log settings loaded from data/%s', SETTING_FILE)
        logger.info("Log level is: %s", log_lvl)