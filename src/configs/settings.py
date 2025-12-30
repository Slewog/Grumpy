from pathlib import Path
from os import getenv
from typing import Optional
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    token: str
    base_dir: Path
    command_prefix: str
    test_guild_id: Optional[int]
    log_level: str = "INFO"


def get_settings() -> Settings:
    base_dir = Path(__file__).resolve().parent.parent.parent
    env_file = base_dir / ".env"

    load_dotenv(dotenv_path=env_file)

    token = getenv("DISCORD_BOT_TOKEN")
    test_guild_raw = getenv("TEST_GUILD_ID")
    command_prefix = str(getenv("COMMAND_PREFIX", "!"))

    if token is None or token == "YOUR_BOT_TOKEN_HERE":
        raise RuntimeError("DISCORD_BOT_TOKEN is not configured in the .env file.")

    test_guild_id = None
    if test_guild_raw:
        try:
            test_guild_id = int(test_guild_raw)
        except ValueError as exc:
            raise RuntimeError("TEST_GUILD_ID is not defined in the .env file") from exc

    return Settings(
        token=token,
        command_prefix=command_prefix,
        base_dir=base_dir,
        test_guild_id=test_guild_id,
    )