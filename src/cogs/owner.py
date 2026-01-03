import discord
from logging import getLogger
from discord.ext import commands
from discord import app_commands

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.bot import Grumpy

class Owner(commands.Cog, name="Owner"):
    """Cog for owner-only commands."""

    def __init__(self, bot: Grumpy) -> None:
        self.bot = bot
        self._logger = getLogger('grumpy.cogs.owner')

        self._logger.info("Owner cog successfully loaded")

    """ @app_commands.command(name="shutdown", description="Shut down the bot.")
    @app_commands.checks.is_owner()
    async def shutdown(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Shutting down...")
        await self.bot.close() """