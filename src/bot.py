import logging
from pathlib import Path
from dataclasses import dataclass
import discord
from discord.ext import commands

from src.services.logging import build_logging
from src.configs import Settings, get_settings, build_intents


class Grumpy(commands.Bot):
    def __init__(self, *, settings: Settings) -> None:
        intents = build_intents()
        self._logger = logging.getLogger('grumpy')
        self.settings = settings
        super().__init__(
            command_prefix=settings.command_prefix,
            intents=intents,
            # description="Grumpy Discord Bot",
        )

    async def setup_hook(self) -> None:
        self._logger.info("Setting up bot...")
        # Load cogs here

    async def on_ready(self) -> None:
        """Called when the bot is ready."""
        all_guilds = self.guilds
        guilds_count = len(all_guilds)

        self._logger.info("Sucessfully logged as %s (CLIENT ID: %s) in %s Guilds", self.user, self.user.id, guilds_count)

        for idx, guild in enumerate(all_guilds, start=1):
            self._logger.debug("Connected on guilds %s/%s (NAME:%s, ID: %s, OWNER: %s, OWNER ID: %s)", idx, guilds_count, guild.name, guild.id, guild.owner, guild.owner_id)

        # Set commands translation here

        # Sync commands here

        await self.change_presence(activity=discord.Game(name="Under development"), status=discord.Status.dnd) 


@dataclass(slots=True)
class GrumpyApp:
    settings: Settings
    bot: Grumpy

    def run(self) -> None:
        self.bot.run(token=self.settings.token)


def create_bot() -> GrumpyApp:
    base_dir = Path(__file__).resolve().parent.parent
    build_logging(base_dir)

    settings = get_settings(logger=logging.getLogger('grumpy.settings'), base_dir=base_dir)

    bot = Grumpy(settings=settings)
    return GrumpyApp(settings=settings, bot=bot)