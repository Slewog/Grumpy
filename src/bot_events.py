from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bot import Grumpy

from .settings import SHUTDOWN_MSG
from discord import Object, HTTPException


async def load_cogs(bot: Grumpy) -> None:
    cogs_dir = bot.settings.base_dir / "src" / "cogs"
    if not cogs_dir.is_dir():
        bot.logger.error(f"Unable to find the cogs directory. {SHUTDOWN_MSG}")
        raise FileNotFoundError(f"An error has been detected in cogs loading. The program will shutdown automatically. {SHUTDOWN_MSG}")

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


async def synchronize_commands(bot: Grumpy) -> None:
    synced: list = []
    test_guild_id = bot.settings.test_guild_id

    bot.logger.info("Starting commands registration.")

    try:
        if bot.is_development() and test_guild_id:
            guild = Object(id=test_guild_id)
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            bot.logger.info(f"{len(synced)} slash commands synchronized in the server {test_guild_id} for development.")
            return

        synced = await bot.tree.sync()
        bot.logger.info(f"{len(synced)} slash commands are synchronized globally (may take some time).")
    except HTTPException as exc:
        bot.logger.error("Command synchronization failed.", exc_info=exc)