from logging import getLogger
from sys import exit as sys_exit
from typing import TYPE_CHECKING
from os import listdir as os_listdir
from discord import Object, HTTPException, Status, Game

from src.cogs import Admin, Owner

if TYPE_CHECKING:
    from src.bot import Grumpy

async def register_cogs(bot: Grumpy) -> None:
    logger = getLogger('grumpy.cogs')

    logger.info("Loading of the 2 cogs has begun.")
    await bot.add_cog(Admin(bot))
    await bot.add_cog(Owner(bot))


async def register_commands(bot: Grumpy) -> None:
    """
    Sync all comands global or for developement guild.

    :param is_dev: if set to True commands will be sync  one guild.
    """
    test_guild_id = bot.settings.test_guild_id
    logger = getLogger('grumpy.cogs')
    synced: list = []

    try:
        if bot.is_dev_mode and test_guild_id:
            guild = Object(id=test_guild_id)
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            logger.info("%s slash commands synchronized on the server %s for development", len(synced), test_guild_id)
        else:
            synced = await bot.tree.sync()
            logger.info("%s slash commands are synchronized globally (may take some time).", len(synced))
    except HTTPException as exc:
        logger.error("Command synchronization failed: %s", exc)


async def setup_presence(bot: Grumpy) -> None:
    BOT_VALID_STATUS = {
        "online": Status.online,
        "offline": Status.offline,
        "idle": Status.idle,
        "dnd": Status.dnd,
        "do_not_disturb": Status.dnd,
        "invisible": Status.invisible,
    }

    await bot.change_presence(
        activity= Game(name= "Under development" if bot.is_dev_mode else bot.settings.activity),
        status= Status.dnd if bot.is_dev_mode else BOT_VALID_STATUS[bot.settings.status]
    )