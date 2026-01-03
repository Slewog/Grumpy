from logging import getLogger
from sys import exit as sys_exit
from typing import TYPE_CHECKING
from os import listdir as os_listdir
from discord import Object, HTTPException

from src.cogs import Admin, Owner

if TYPE_CHECKING:
    from src.bot import Grumpy

async def register_cogs(bot: Grumpy):
    logger = getLogger('grumpy.cogs')
    cogs: list[str] = []
    cogs_count = None

    try:
        cogs = os_listdir(bot.settings.base_dir / "src" / "cogs")

        cogs.remove('__pycache__')
        cogs.remove('__init__.py')
        cogs_count = len(cogs)
    except ValueError:
        logger.warning("Unable to remove the 'cogs/__pycache__/' folder, perhaps it doesn't exist.")
        cogs_count = len(cogs) - 2
    except FileNotFoundError as exc:
        logger.exception("The cogs folder doens't exist. The bot wil shut down automatically", exc_info=exc)
        sys_exit()

    logger.info("Loading of cogs has begun, there are %s of them.,", cogs_count)
    await bot.add_cog(Admin(bot))
    await bot.add_cog(Owner(bot))


async def register_commands(bot: Grumpy):
    test_guild_id = bot.settings.test_guild_id
    logger = getLogger('grumpy.cogs')
    synced: list = []

    try:
        if test_guild_id:
            guild = Object(id=test_guild_id)
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            logger.info("Slash commands synchronized on the server %s", test_guild_id)
        else:
            synced = await bot.tree.sync()
            logger.info("Slash commands are synchronized globally (may take some time).")
    except HTTPException as exc:
        logger.error("Command synchronization failed: %s", exc)

    logger.info("%s slash commands synchronized", len(synced))