import platform
from pathlib import Path
from logging import Logger
from os import name as os_name
from dataclasses import dataclass

import discord
from discord.ext import commands

from .services.logger import build_logger, get_log_level_name
from .settings import get_intents, get_settings, Settings, SHUTDOWN_MSG
from .bot_events import load_cogs, synchronize_commands
from .utils import BOT_VALID_STATUS


class Grumpy(commands.Bot):
    def __init__(self, logger: Logger, settings: Settings) -> None:
        super().__init__(
            command_prefix= commands.when_mentioned_or(settings.command_prefix),
            intents= get_intents()
        )

        self.settings = settings
        self.logger = logger

    def is_development(self) -> bool:
        return self.settings.is_dev_mode

    async def setup_hook(self) -> None:
        await load_cogs(self)

    async def on_ready(self) -> None:
        # Tell the type checker that this is a ClientUser.
        assert isinstance(self.user, discord.ClientUser)

        self.logger.info(f"Successfully logged in as {self.user} in {len(self.guilds)} guilds")

        # await self.tree.set_translator(CommandsTranslator())
        # self.logger.info("Commands translations system has been loaded.")

        await synchronize_commands(self)

        is_development = self.is_development()
        await self.change_presence(
            activity= discord.Game(name= "Under development" if is_development else self.settings.activity),
            status= discord.Status.dnd if is_development else BOT_VALID_STATUS[self.settings.status]
        )

        self.logger.info(f"{self.user.name} is ready to use.")


@dataclass(slots=True)
class GrumpyApp:
    token: str
    bot: Grumpy

    def run(self) -> None:
        self.bot.run(token=self.token)


def create_bot() -> GrumpyApp:
    base_dir = Path(__file__).resolve().parent.parent

    logger = build_logger(base_dir)
    token, settings = get_settings(base_dir=base_dir, logger=logger)

    logger.info(f"Log level: {get_log_level_name(logger.getEffectiveLevel())}")
    logger.info(f"discord.py API version: {discord.__version__}")
    logger.info(f"Python version: {platform.python_version()}")
    logger.info(f"Running on: {platform.system()} {platform.release()} ({os_name})")
    logger.info("-------------------")

    bot = Grumpy(logger, settings)
    return GrumpyApp(token, bot)
