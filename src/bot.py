import platform
from pathlib import Path
from logging import Logger
from os import name as os_name
from dataclasses import dataclass

import discord
from discord.ext import commands

from .utils import BOT_VALID_STATUS
from .settings import get_settings, Settings
from .services.commands_translator import CommandsTranslator
from .services.logger import build_logger, get_log_level_name
from .bot_events import load_cogs, synchronize_slash_commands


class Grumpy(commands.Bot):
    def __init__(self, logger: Logger, settings: Settings) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        self.settings = settings
        self.logger = logger

        super().__init__(
            command_prefix = commands.when_mentioned_or(settings.command_prefix),
            intents = intents,
            help_command = None
        )

    def is_development(self) -> bool:
        return self.settings.is_dev_mode

    async def get_command_translation(self, locale_str: str, user_locale: discord.Locale) -> str:
        translation = await self.tree.translator.translate(
            discord.app_commands.locale_str(locale_str),
            user_locale,
            None
        )

        return translation.partition("\n")[0] if translation is not None else locale_str.partition("\n")[0]

    async def setup_hook(self) -> None:
        await load_cogs(self)

    async def on_ready(self) -> None:
        # Tell the type checker that this is a ClientUser.
        assert isinstance(self.user, discord.ClientUser)

        self.logger.info(f"Successfully logged in as {self.user} in {len(self.guilds)} guilds")

        await self.tree.set_translator(CommandsTranslator())
        self.logger.info("The slash command translation service has been successfully loaded.")

        is_development = self.is_development()

        if is_development:
            await synchronize_slash_commands(self)

        await self.change_presence(
            activity= discord.Game(name= "Under development" if is_development else self.settings.activity),
            status= discord.Status.dnd if is_development else BOT_VALID_STATUS[self.settings.status]
        )

        self.logger.info(f"{self.user.name} is ready to use.")

    async def on_disconnect(self) -> None:
        self.logger.warning("The bot disconnects following a request from its owner.")

    async def on_guild_join(self, guild: discord.Guild) -> None:
        print(f'Joined guild: {guild.name} (ID: {guild.id})')

    async def on_guild_remove(self, guild: discord.Guild) -> None:
        print(f'Removed from guild: {guild.name} (ID: {guild.id})')

    async def on_member_join(self, member: discord.Member) -> None:
        print(f"{member.display_name} as joined {member.guild.name}")

    async def on_member_remove(self, member: discord.Member) -> None:
        print(f"{member.display_name} as leaved {member.guild.name}")

    async def on_raw_member_remove(self, payload: discord.RawMemberRemoveEvent):
        pass


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
