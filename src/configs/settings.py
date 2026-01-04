from os import getenv
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from logging import Logger, DEBUG
from dataclasses import dataclass

from src.utils import load_json_file

ENV_FILE_NAME = ".env"
SETTING_FILE = "data/cfg/grumpy.json"
BOT_TOKEN_DEFAULT = "YOUR_BOT_TOKEN_HERE"
BOT_TEST_GUILD_ID = "YOUR_TEST_GUILD_ID_HERE"
BOT_LINK_INVITE_DEFAULT = "YOUR_BOT_INVITE_LINK_HERE"
BOT_LINK_INVITE_PATTERN = "https://discord.com/oauth2/authorize"

@dataclass(slots=True)
class Settings:
    token: str
    status: str
    activity: str
    base_dir: Path
    invite_link: str
    is_dev_mode: bool
    command_prefix: str
    test_guild_id: Optional[int]


def get_settings_from_json(json_file: Path):
    """
    :param json_file: grumpy.json dir path
    :type json_file: Path
    :param logger: Bot logger system
    :type logger: Logger
    """
    if not json_file.is_file():
        raise RuntimeError(f"Unable to access the settings files in {SETTING_FILE}, the program will shut down automatically.")

    return load_json_file(json_file)


def get_env_file_path(base_dir: Path, logger: Logger) -> Path:
    """
    :param base_dir: Current bot directory path
    :type base_dir: str
    :param logger: Bot logger system
    :type logger: Logger
    """
    env_file_path = base_dir / ENV_FILE_NAME

    if not env_file_path.is_file():
        logger.error("The %s file could not be found in the bot's root directory.", ENV_FILE_NAME)
        raise RuntimeError(f"Unable to access bot settings, the program will shut down automatically.")

    return env_file_path


def check_and_convert_link(raw_link: str, logger: Logger) -> str:
    """
    :param raw_link: Bot invitation link
    :type raw_link: str
    :param logger: Bot logger system
    :type logger: Logger
    """
    if raw_link == BOT_LINK_INVITE_DEFAULT or not BOT_LINK_INVITE_PATTERN in raw_link:
        logger.error("'INVITE_LINK' is nor set. Please verify that it is correctly defined in the %s file", ENV_FILE_NAME)
        raise RuntimeError(f"An error has been detected in the settings, the program will shut down automatically.")

    return raw_link


def check_and_convert_token(raw_token: str, logger: Logger) -> str:
    """
    :param raw_token: Bot discord token
    :type raw_token: str
    :param logger: Bot logger system
    :type logger: Logger
    """
    if raw_token == BOT_TOKEN_DEFAULT:
        logger.error("'DISCORD_BOT_TOKEN' is nor set and it's needed to launch the bot, please verify that it is correctly defined in the %s file", ENV_FILE_NAME)
        raise RuntimeError(f"An error has been detected in the settings, the program will shut down automatically.")

    return raw_token


def convert_test_guild_id(raw_id: str, logger: Logger) -> int | None:
    """
    :param raw_id: GUILD ID FOR DEVELOPMENT
    :type raw_id: str
    :param logger: Bot logger system
    :type logger: Logger
    """
    if raw_id == BOT_TEST_GUILD_ID:
        logger.warning("'TEST_GUILD_ID' is nor set and it's needed to sync commands to a guild on DEVELOPMENT Mode. Please verify that it is correctly defined in the %s file.", ENV_FILE_NAME)
        return None

    valid_id = None
    try:
        valid_id = int(raw_id)
    except (ValueError, TypeError):
        logger.warning("Unable to convert 'TEST_GUILD_ID' it's needed to sync commands to a guild on DEVELOPMENT Mode. Please verify that it is correctly defined in the %s file.", ENV_FILE_NAME)
        return None

    return valid_id


def check_status(raw_status: str, logger: Logger) -> str:
    """
    :param raw_status: bot status
    :type raw_status: str
    :param logger: Bot logger system
    :type logger: Logger
    """
    BOT_STATUS = ["online", "offline", "idle", "dnd", "do_not_disturb", "invisible"]

    if not raw_status in BOT_STATUS:
        return "online"

    return raw_status


def is_development(is_dev: str) -> bool:
    """
    :param is_dev: 'True' or 'False'
    :type is_dev: str
    """
    capitalized = is_dev.capitalize()
    if capitalized in ["True", "False"]:
        return bool(capitalized)

    return False


def get_settings(base_dir: Path, logger: Logger) -> Settings:
    """
    :param base_dir: Current bot directory path
    :type base_dir: Path
    :param logger: Bot logger system
    :type logger: Logger
    """

    settings_dict = get_settings_from_json(base_dir / SETTING_FILE)
    logger.info("Successfully loaded settings from '%s'", SETTING_FILE)

    env_file = get_env_file_path(base_dir, logger)
    load_dotenv(dotenv_path=env_file, encoding="utf-8-sig")
    logger.info("Successfully loaded settings from environment variables file")

    test_guild_id = None
    command_prefix: str = settings_dict.get("command_prefix", "!")
    activity: str = settings_dict.get("activity", "Listening !help")
    status = check_status(settings_dict.get("status", "online"), logger)
    token = check_and_convert_token(getenv("DISCORD_BOT_TOKEN", BOT_TOKEN_DEFAULT), logger)
    invite_link = check_and_convert_link(getenv("INVITE_LINK", BOT_LINK_INVITE_DEFAULT), logger)

    is_dev_mode = is_development(getenv("IS_DEV", "False"))
    if is_dev_mode:
        test_guild_id = convert_test_guild_id(getenv("TEST_GUILD_ID", BOT_TEST_GUILD_ID), logger)
        logger.setLevel(DEBUG)
        logger.info("The bot is loaded in DEVELOPMENT Mode, logging has been set to DEBUG")

    logger.info("Invite link - Defined.")
    logger.info("Server Development ID - %s.", test_guild_id if test_guild_id is not None else "Undefined")

    return Settings(
        token = token,
        is_dev_mode = is_dev_mode,
        base_dir = base_dir,
        invite_link = invite_link,
        command_prefix =command_prefix,
        test_guild_id  = test_guild_id,
        activity = activity,
        status = status
    )