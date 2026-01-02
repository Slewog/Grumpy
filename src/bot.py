import logging
# import logging.config
from pathlib import Path
from dataclasses import dataclass
from discord.ext import commands

from src.services.logging import build_logging
from src.configs import Settings, get_settings, build_intents

@dataclass(slots=True)
class GrumpyApp:
    settings: Settings
    bot: commands.Bot

    def run(self) -> None:
        self.bot.run(token=self.settings.token)


class Grumpy(commands.Bot):
    def __init__(self, *, settings: Settings) -> None:
        intents = build_intents()
        super().__init__(
            command_prefix=settings.command_prefix,
            intents=intents,
            # description="Grumpy Discord Bot",
        )

    async def setup_hook(self) -> None:
        print("Setting up bot...")
        # Load cogs here

    async def on_ready(self) -> None:
        """Called when the bot is ready."""
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        # Set commands translation here
        # Sync commands here

def create_bot() -> GrumpyApp:
    base_dir = Path(__file__).resolve().parent.parent
    build_logging(base_dir)
    logger = logging.getLogger('BOT')

    settings = get_settings(logger=logger, base_dir=base_dir)

    if settings.test_guild_id:
        logger.info("Development server ID: %s", settings.test_guild_id)

    bot = Grumpy(settings=settings)
    return GrumpyApp(settings=settings, bot=bot)