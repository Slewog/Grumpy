from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.bot import Grumpy

import discord
from logging import getLogger
from discord.ext import commands
from discord import app_commands


class Admin(commands.Cog, name="Admin"):
    """Cog for owner-only commands."""

    def __init__(self, bot: Grumpy) -> None:
        self.bot = bot
        self._logger = getLogger('grumpy.admin')

        self._logger.debug("Admin cog successfully loaded.")

    @app_commands.command(name="purge", description="Purge a text channel")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction) -> None:
        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message("This command can only be used in text channels.")
            return

        await interaction.response.send_message("I will purge this channel",ephemeral=True)
        await interaction.channel.purge(limit=100)

    """ @app_commands.command(name="delete_message", description="Delete a number of message in a text channel.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(amount="Message amount to delete")
    async def delete_message(self, interaction: discord.Interaction, amount: int):
        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message("This command can only be used in text channels.", ephemeral=True)
            return

        messages = [message async for message in interaction.channel.history(limit=amount if amount <= 100 else 100)]
        total_msg_find = len(messages)

        if total_msg_find == 0:
            await interaction.response.send_message("No messages have been deleted", ephemeral=True)
            return

        await interaction.response.send_message(f"I will delete {total_msg_find} messages from this channel", ephemeral=True)
        await interaction.channel.delete_messages(messages) """

    async def cog_app_command_error(self, interaction, error: Exception) -> None:
        cmd = interaction.command
        print(f'An error occurred in the Admin cog !\n- Slash Command: {cmd.name}\n- Error: {error} ({type(error)})')

    async def cog_command_error(self, ctx: commands.Context, error: Exception) -> None:
        print(f'An error occurred in the Admin cog !\n- Command: {ctx.invoked_with.upper()}\n- Error: {error} ({type(error)})')

        if isinstance(error, commands.errors.MissingPermissions):
            if ctx.invoked_with in ["clear", "purge"]:
                await ctx.send(f"{ctx.author.mention} you do not have the required permissions to manage messages.", ephemeral=True)
                return