from os import getenv
from pathlib import Path
from logging import Logger
from typing import Optional
from dotenv import load_dotenv
from dataclasses import dataclass

ENV_FILE_NAME = ".env"
BOT_LINK_INVITE_DEFAULT = "YOUR_BOT_INVITE_LINK_HERE"
BOT_TOKEN_DEFAULT = "YOUR_BOT_TOKEN_HERE"

@dataclass(slots=True)
class Settings:
    token: str
    base_dir: Path
    invite_link: str
    test_guild_id: Optional[int]
    command_prefix: str = "!"


def check_and_convert_link(raw_link: str | None, logger: Logger) -> str:
    if raw_link is None or raw_link == BOT_LINK_INVITE_DEFAULT:
        logger.error("Unable to obtain 'INVITE_LINK, please verify that it is correctly defined in the %s file", ENV_FILE_NAME)
        raise RuntimeError(f"An error has been detected in the settings, the program will shut down automatically.")

    return raw_link


def check_and_convert_token(raw_token: str | None, logger: Logger) -> str:
    if raw_token is None or raw_token == BOT_TOKEN_DEFAULT:
        logger.error("Unable to obtain 'DISCORD_BOT_TOKEN', please verify that it is correctly defined in the %s file", ENV_FILE_NAME)
        raise RuntimeError(f"An error has been detected in the settings, the program will shut down automatically.")

    return raw_token


def convert_test_guild_id(raw_id: str | None, logger: Logger) -> int | None:
    if raw_id is None:
        logger.warning("Unable to obtain 'TEST_GUILD_ID'. Please verify that it is correctly defined in the %s file.", ENV_FILE_NAME)
        return None

    valid_id = None
    try:
        valid_id = int(raw_id)
    except (ValueError, TypeError) as exc:
        logger.warning("Unable to convert 'TEST_GUILD_ID'. Please verify that it is correctly defined in the %s file.", ENV_FILE_NAME)
        return None

    return valid_id


def get_settings(logger: Logger, base_dir: Path) -> Settings:
    env_file = base_dir / ENV_FILE_NAME

    if not env_file.is_file():
        logger.error("The %s file could not be found in the bot's root directory.", ENV_FILE_NAME)
        raise RuntimeError(f"Unable to access bot settings, the program will shut down automatically.")

    load_dotenv(dotenv_path=env_file, encoding="utf-8-sig")

    token_raw = getenv("DISCORD_BOT_TOKEN")
    invite_link_raw = getenv("INVITE_LINK")
    test_guild_id_raw = getenv("TEST_GUILD_ID")

    logger.info("Loading settings from %s", ENV_FILE_NAME)

    token = check_and_convert_token(token_raw, logger)
    invite_link = check_and_convert_link(invite_link_raw, logger)
    test_guild_id = convert_test_guild_id(test_guild_id_raw, logger)

    logger.info("Server Development ID - %s.", test_guild_id if test_guild_id is not None else "Undefined")
    logger.info("Invite link - Defined.")

    logger.info("Settings loaded from %s with success.", ENV_FILE_NAME)

    return Settings(
        token=token,
        base_dir=base_dir,
        invite_link=invite_link,
        test_guild_id=test_guild_id
    )