from pathlib import Path
from os import getenv
from typing import Optional
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    token: str
    base_dir: Path
    invite_link: str
    test_guild_id: Optional[int]
    client_id: Optional[int]
    command_prefix: str = "!"


def get_settings() -> Settings:
    base_dir = Path(__file__).resolve().parent.parent.parent
    env_file = base_dir / ".env"

    load_dotenv(dotenv_path=env_file)

    token = getenv("DISCORD_BOT_TOKEN")
    test_guild_raw = getenv("TEST_GUILD_ID")
    client_id_raw = getenv("CLIENT_ID")
    invite_link = getenv("INVITE_LINK")

    if invite_link is None or invite_link == "YOUR_BOT_INVITE_LINK_HERE":
        raise RuntimeError("INVITE_LINK is not configured in the .env file.")

    if token is None or token == "YOUR_BOT_TOKEN_HERE":
        raise RuntimeError("DISCORD_BOT_TOKEN is not configured in the .env file.")

    client_id = None
    if client_id_raw:
        try:
            client_id = int(client_id_raw)
        except ValueError as exc:
            raise RuntimeError("CLIENT_ID need to be an integer in the .env file") from exc

    test_guild_id = None
    if test_guild_raw:
        try:
            test_guild_id = int(test_guild_raw)
        except ValueError as exc:
            raise RuntimeError("TEST_GUILD_ID is not defined in the .env file") from exc

    return Settings(
        token=token,
        base_dir=base_dir,
        invite_link=invite_link,
        test_guild_id=test_guild_id,
        client_id = client_id,
    )