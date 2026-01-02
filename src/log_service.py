import json
import logging
import logging.config
from pathlib import Path


def build_logging(base_dir: Path):
    settings_path = base_dir / "data" / "logging_settings.json"
    config_dict = {}

    try:
        with settings_path.open("r", encoding="utf-8-sig") as fp:
            config_dict = json.load(fp)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Logging service settings failed to load") from exc

    logging.config.dictConfig(config_dict)