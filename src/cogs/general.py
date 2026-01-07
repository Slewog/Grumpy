import discord
from logging import getLogger
from discord.ext import commands
from discord import app_commands

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.bot import Grumpy


class General(commands.Cog, name="General"):
    """Cog for owner-only commands."""

    def __init__(self, bot: Grumpy) -> None:
        self.bot = bot
        self._logger = getLogger('grumpy.general')

        self._logger.debug("General cog successfully loaded.")

    @app_commands.command(name="ping", description="Check if the bot is alive.")
    async def ping(self, interaction: discord.Interaction) -> None:
        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message("This command can only be used in text channels.")
            return

        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=discord.Color.purple(),
        )

        await interaction.response.send_message(embed=embed)
    async def cog_app_command_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message( f"An error occurred in the General COG: {error}.", ephemeral=True )
        print(error)
        """ if isinstance(error, commands.errors.NotOwner):
            pass """