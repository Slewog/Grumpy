import json
from typing import  Any
from pathlib import Path


def load_json_file(json_file: Path) -> dict[str, Any]:
    """
    Loads the settings json file.

    :param base_dir: Current directory of the bot.
    """
    tmp_dict = {}

    try:
        with json_file.open("r", encoding="utf-8-sig") as fp:
            tmp_dict = json.load(fp)
    except json.JSONDecodeError:
        raise RuntimeWarning(f"JSON FILE ERROR - Unable to decode the file: '{json_file}'")
    except FileNotFoundError:
        raise RuntimeError(f"JSON FILE ERROR - File not found: '{json_file}'")

    return tmp_dict