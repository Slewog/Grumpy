from logging import getLogger
from typing import TYPE_CHECKING
from discord import Object, HTTPException

from src.cogs import Admin, Owner

if TYPE_CHECKING:
    from src.bot import Grumpy


async def register_cogs(bot: Grumpy) -> None:
    logger = getLogger('grumpy.cogs')

    logger.info("Loading of the 2 cogs has begun.")
    await bot.add_cog(Admin(bot))
    await bot.add_cog(Owner(bot))


async def register_commands(bot: Grumpy) -> None:
    test_guild_id = bot.get_test_guild_id()
    logger = getLogger('grumpy.cogs')
    synced: list = []

    try:
        if bot.is_development() and test_guild_id:
            guild = Object(id=test_guild_id)
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            logger.info("%s slash commands synchronized on the server %s for development", len(synced), test_guild_id)
            return

        synced = await bot.tree.sync()
        logger.info("%s slash commands are synchronized globally (may take some time).", len(synced))
    except HTTPException as exc:
        logger.error("Command synchronization failed: %s", exc_info=exc)