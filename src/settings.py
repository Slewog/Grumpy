from os import getenv
from pathlib import Path
from discord import Intents
from dotenv import load_dotenv
from logging import Logger, DEBUG
from dataclasses import dataclass
from typing import Optional, Literal, Any


from .utils import load_json_file, BOT_VALID_STATUS

ENV_FILE_NAME = ".env"
SETTINGS_DIR = "data/cfg"
SETTINGS_FILE = "grumpy.json"
BOT_TOKEN_DEFAULT = "YOUR_BOT_TOKEN_HERE"
BOT_TEST_GUILD_ID = "YOUR_TEST_GUILD_ID_HERE"
BOT_LINK_INVITE_DEFAULT = "YOUR_BOT_INVITE_LINK_HERE"

SHUTDOWN_MSG = "The program will shutdown automatically."
AUTO_SHUTDOWN_MSG = f"An error has been detected in the settings. {SHUTDOWN_MSG}"


@dataclass(slots=True)
class Settings:
    status: str
    activity: str
    base_dir: Path
    invite_link: str
    is_dev_mode: bool
    command_prefix: str
    test_guild_id: Optional[int]


def get_intents() -> Intents:
    intents = Intents.default()
    intents.message_content = True
    intents.members = True
    intents.reactions = True
    intents.guilds = True

    return intents


def get_settings_from_json(json_file: Path, logger: Logger) -> dict[str, Any]:
    if not json_file.is_file():
        logger.error(f"The settings file could not be found in the bot's '{SETTINGS_DIR}' directory. {SHUTDOWN_MSG}")
        raise FileNotFoundError(AUTO_SHUTDOWN_MSG)

    return load_json_file(json_file)


def get_env_file_path(base_dir: Path, logger: Logger) -> Path:
    env_file_path = base_dir / ENV_FILE_NAME

    if not env_file_path.is_file():
        logger.error(f"The environment variables file could not be found in the bot's root directory. {SHUTDOWN_MSG}")
        raise FileNotFoundError(AUTO_SHUTDOWN_MSG)

    return env_file_path


def check_and_convert_link(raw_invite_link: str, logger: Logger) -> str:
    BOT_LINK_INVITE_PATTERN = "https://discord.com/oauth2/authorize"

    if raw_invite_link == BOT_LINK_INVITE_DEFAULT or not BOT_LINK_INVITE_PATTERN in raw_invite_link:
        logger.error(f"'INVITE_LINK' is not set. Please verify that it is correctly defined in the {ENV_FILE_NAME} file.")
        raise ValueError(AUTO_SHUTDOWN_MSG)

    return raw_invite_link


def check_and_convert_token(raw_bot_token: str, logger: Logger) -> str:
    if raw_bot_token == BOT_TOKEN_DEFAULT:
        logger.error(f"'DISCORD_BOT_TOKEN' is not set and it's needed to launch the bot, please verify that it is correctly defined in the {ENV_FILE_NAME} file.")
        raise ValueError(AUTO_SHUTDOWN_MSG)

    return raw_bot_token


def convert_test_guild_id(raw_guild_id: str, logger: Logger) -> int | None:
    if raw_guild_id == BOT_TEST_GUILD_ID:
        logger.warning(f"'TEST_GUILD_ID' is not set and it's needed to sync commands to a guild on DEVELOPMENT Mode. Please verify that it is correctly defined in the {ENV_FILE_NAME} file.")
        return None

    valid_id = None
    try:
        valid_id = int(raw_guild_id)
    except (ValueError, TypeError):
        logger.warning(f"Unable to convert 'TEST_GUILD_ID' it's needed to sync commands to a guild on DEVELOPMENT Mode. Please verify that it is correctly defined in the {ENV_FILE_NAME} file.")
        return None

    return valid_id


def check_status(raw_status: Literal["online", "offline", "idle", "dnd", "do_not_disturb", "invisible"], logger: Logger) -> str:
    s = str(raw_status).strip().lower()

    if not s in BOT_VALID_STATUS.keys():
        logger.warning(f"Invalid status '{raw_status}', fallback to 'online'.")
        return "online"

    return s


def is_development(is_dev: Literal["True", "true", "False", "false"]) -> bool:
    capitalized = is_dev.capitalize()
    if capitalized in ["True", "False"]:
        return bool(capitalized)

    return False


def get_settings(base_dir: Path, logger: Logger):
    settings_dict = get_settings_from_json(base_dir / SETTINGS_DIR / SETTINGS_FILE, logger)

    env_file = get_env_file_path(base_dir, logger)
    load_dotenv(dotenv_path=env_file, encoding="utf-8-sig")
    logger.info(f"Successfully loaded settings from environment variables file and from '{SETTINGS_DIR}/{SETTINGS_FILE}'.")

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

    return token, Settings(
        is_dev_mode = is_dev_mode,
        base_dir = base_dir,
        invite_link = invite_link,
        command_prefix =command_prefix,
        test_guild_id  = test_guild_id,
        activity = activity,
        status = status
    )