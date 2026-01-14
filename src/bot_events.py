from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bot import Grumpy

from .settings import SHUTDOWN_MSG
from discord import HTTPException, Guild


async def load_cogs(bot: Grumpy) -> None:
    cogs_dir = bot.settings.base_dir / "src/cogs"
    if not cogs_dir.is_dir():
        bot.logger.error(f"An error has been detected: unable to find the cogs directory. {SHUTDOWN_MSG}")
        raise FileNotFoundError(f"An error has been detected in cogs loading. {SHUTDOWN_MSG}")

    cogs = [file.name for file in cogs_dir.glob('*.py')]
    cogs_count = len(cogs)

    for i, cog in enumerate(cogs, start=1):
        extension = cog[:-3]
        try:
            await bot.load_extension(f"src.cogs.{extension}")
            bot.logger.info(f"Loaded extension {i}/{cogs_count}: '{extension}'")
        except ModuleNotFoundError as exc:
            exception = f"{type(exc).__name__}: {exc}"
            bot.logger.error(f"Failed to load extension '{extension}'\n{exception}")


async def synchronize_slash_commands(bot: Grumpy) -> None:
    bot.logger.info("Slash commands synchronization begins. They will be synchronize for a test server")

    synced: list = []
    test_guild_id = bot.settings.test_guild_id

    if test_guild_id is None:
        bot.logger.warning("Unable to synchronize slash commands for development. The test server ID is not defined in the environment variables file")
        return

    guild = bot.get_guild(test_guild_id)

    if guild is None:
        bot.logger.warning(f"Unable to synchronize slash commands for development. I have not been added to the test server (ID:{test_guild_id})")

    assert isinstance(guild, Guild)

    try:
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        bot.logger.info(f"{len(synced)} slash commands have been successfully synchronized in the '{guild.name}' server")
    except HTTPException as exc:
        bot.logger.error("Slash command synchronization failed.", exc_info=exc)