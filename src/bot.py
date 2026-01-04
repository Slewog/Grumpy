import discord
from pathlib import Path
from logging import getLogger
from dataclasses import dataclass
from discord.ext import commands

from src.services import build_logging
from src.configs import build_intents, get_settings, Settings
from src.bot_events import register_cogs, register_commands

class Grumpy(commands.Bot):
    def __init__(self, settings: Settings, intents: discord.Intents) -> None:
        self._logger = getLogger('grumpy')
        self.settings = settings
        self.is_dev_mode = self.settings.is_dev_mode
        super().__init__(
            command_prefix= commands.when_mentioned_or(settings.command_prefix),
            intents= intents,
            # description="Grumpy Discord Bot",
        )
        self._logger.debug("Grumpy has been initialized")

    async def setup_hook(self) -> None:
        await register_cogs(self)

    async def on_ready(self) -> None:
        all_guilds = self.guilds
        guilds_count = len(all_guilds)

        self._logger.info("Sucessfully logged as %s (CLIENT ID: %s) in %s Guilds", self.user, self.user.id, guilds_count)

        for idx, guild in enumerate(all_guilds, start=1):
            self._logger.debug("Connected on guilds %s/%s (NAME:%s, ID: %s, OWNER: %s, OWNER ID: %s)", idx, guilds_count, guild.name, guild.id, guild.owner, guild.owner_id)

        # Set commands translation here

        await register_commands(self)

        status = None
        if self.settings.status == "online":
            status = discord.Status.online
        elif self.settings.status == "offline":
            status = discord.Status.offline
        elif self.settings.status == "idle":
            status = discord.Status.idle
        elif self.settings.status in ["dnd", "do_not_disturb"]:
            status = discord.Status.dnd
        elif self.settings.status == "invisible":
            status = discord.Status.invisible

        await self.change_presence(
            activity= discord.Game(name= "Under development" if self.is_dev_mode else self.settings.activity),
            status= discord.Status.dnd if self.is_dev_mode else status
        )



@dataclass(slots=True)
class GrumpyApp:
    settings: Settings
    bot: Grumpy

    def run(self) -> None:
        self.bot.run(token=self.settings.token)


def create_bot() -> GrumpyApp:
    base_dir = Path(__file__).resolve().parent.parent

    logger = build_logging(base_dir)
    settings = get_settings(base_dir=base_dir, logger=logger)
    intents = build_intents()

    bot = Grumpy(settings, intents)
    return GrumpyApp(settings= settings, bot= bot)