from os import getenv
from pathlib import Path
from logging import Logger
from typing import Optional
from dotenv import load_dotenv
from dataclasses import dataclass

ENV_FILE_NAME = ".env"

@dataclass(slots=True)
class Settings:
    token: str
    base_dir: Path
    invite_link: str
    test_guild_id: Optional[int]
    client_id: Optional[int]
    command_prefix: str = "!"


def get_settings(logger: Logger, base_dir: Path) -> Settings:
    env_file = base_dir / ENV_FILE_NAME

    load_dotenv(dotenv_path=env_file, encoding="utf-8-sig")

    token = getenv("DISCORD_BOT_TOKEN")
    test_guild_raw = getenv("TEST_GUILD_ID")
    client_id_raw = getenv("CLIENT_ID")
    invite_link = getenv("INVITE_LINK")

    logger.info("Loading bot settings from %s", ENV_FILE_NAME)

    if invite_link is None or invite_link == "YOUR_BOT_INVITE_LINK_HERE":
        logger.error('INVITE_LINK is not configured in the .%s file', ENV_FILE_NAME)
        raise RuntimeError(f"INVITE_LINK is not configured in the {ENV_FILE_NAME} file.")

    if token is None or token == "YOUR_BOT_TOKEN_HERE":
        logger.error('DISCORD_BOT_TOKEN is not configured in the %s file', ENV_FILE_NAME)
        raise RuntimeError(f"DISCORD_BOT_TOKEN is not configured in the {ENV_FILE_NAME} file.")

    client_id = None
    if client_id_raw:
        try:
            client_id = int(client_id_raw)
        except ValueError as exc:
            logger.exception("CLIENT_ID is not an integer in the %s file", ENV_FILE_NAME, exc_info=exc)
            raise RuntimeError(f"CLIENT_ID need to be an integer in the {ENV_FILE_NAME} file") from exc

    test_guild_id = None
    if test_guild_raw:
        try:
            test_guild_id = int(test_guild_raw)
        except ValueError as exc:
            logger.exception("TEST_GUILD_ID is not an integer in the %s file", ENV_FILE_NAME, exc_info=exc)
            raise RuntimeError(f"TEST_GUILD_ID need to be an integer in the {ENV_FILE_NAME} file") from exc

    logger.info("Bot settings loaded from %s with success", ENV_FILE_NAME)

    return Settings(
        token=token,
        base_dir=base_dir,
        invite_link=invite_link,
        test_guild_id=test_guild_id,
        client_id = client_id,
    )