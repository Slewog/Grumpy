import discord
from pathlib import Path
from typing import Literal
from logging import Logger
from dataclasses import dataclass
from discord.ext import commands

from src.utils import BOT_VALID_STATUS
from src.services import build_logging, CommandsTranslator
from src.configs import build_intents, get_settings, Settings
from src.bot_events import register_cogs, register_commands

class Grumpy(commands.Bot):
    def __init__(self, settings: Settings, intents: discord.Intents, logger: Logger) -> None:
        # self._logger = logger
        self.settings = settings
        self._logger_level_dict = {
            "DEBUG": logger.debug,
            "INFO": logger.info,
            "WARNING": logger.warning,
            "ERROR": logger.error
        }

        super().__init__(
            command_prefix= commands.when_mentioned_or(settings.command_prefix),
            intents= intents
        )
        self.log("Grumpy has been initialized")

    async def setup_hook(self) -> None:
        await register_cogs(self)

    async def on_ready(self) -> None:
        all_guilds = self.guilds
        guilds_count = len(all_guilds)
        is_development = self.is_development()

        self.log("Sucessfully logged as %s (CLIENT ID: %s) in %s Guilds", self.user, self.user.id, guilds_count)

        if is_development:
            for idx, guild in enumerate(all_guilds, start=1):
                self.log("Connected on guilds %s/%s (NAME:%s, ID: %s, OWNER: %s, OWNER ID: %s)", idx, guilds_count, guild.name, guild.id, guild.owner, guild.owner_id, level="DEBUG")

        await self.tree.set_translator(CommandsTranslator())
        self.log("Commands translations system has been loaded")

        await register_commands(self)

        await self.change_presence(
            activity= discord.Game(name= "Under development" if is_development else self.settings.activity),
            status= discord.Status.dnd if is_development else BOT_VALID_STATUS[self.settings.status]
        )

    def get_test_guild_id(self):
        return self.settings.test_guild_id

    def is_development(self) -> bool:
        return self.settings.is_dev_mode

    def log(self, message: str, *args, level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]="INFO", **kwargs) -> None:
        self._logger_level_dict[level](message, *args, **kwargs)


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

    bot = Grumpy(settings, intents, logger)
    return GrumpyApp(settings= settings, bot= bot)