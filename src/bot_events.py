from logging import getLogger
from typing import TYPE_CHECKING
from discord import Object, HTTPException

from src.cogs import Admin, Owner, General

if TYPE_CHECKING:
    from src.bot import Grumpy


async def register_cogs(bot: Grumpy) -> None:
    bot.log("Cogs loading will start, there are 3 cogs to load.")
    await bot.add_cog(Admin(bot))
    await bot.add_cog(Owner(bot))
    await bot.add_cog(General(bot))


async def synchronize_commands(bot: Grumpy) -> None:
    test_guild_id = bot.get_test_guild_id()
    synced: list = []

    bot.log("Commands registration is starting.")

    try:
        if bot.is_development() and test_guild_id:
            guild = Object(id=test_guild_id)
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            bot.log("%s slash commands synchronized on the server %s for development.", len(synced), test_guild_id)
            return

        synced = await bot.tree.sync()
        bot.log("%s slash commands are synchronized globally (may take some time).", len(synced))
    except HTTPException as exc:
        bot.log("Command synchronization failed: %s.", level="ERROR", exc_info=exc)