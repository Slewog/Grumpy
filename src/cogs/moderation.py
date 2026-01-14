from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import Grumpy

import discord
from discord.ext import commands
from discord import app_commands

DELETE_AFTER = 1.5


class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot: Grumpy) -> None:
        self.bot = bot

    async def _can_perform_in_channel(self, interaction: discord.Interaction, channel_type: str) -> bool:
        can_perform = True
        if channel_type == "text" and not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message("This command can only be used in text channels.", ephemeral=True, delete_after=DELETE_AFTER)
            can_perform = False

        return can_perform

    @app_commands.command(name="purge-channel", description=app_commands.locale_str("purge_desc"))
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge_channel(self, interaction: discord.Interaction) -> None:
        if not await self._can_perform_in_channel(interaction, "text"):
            return

        assert isinstance(interaction.channel, discord.TextChannel)

        await interaction.response.send_message("I will purge this channel", ephemeral=True, delete_after=DELETE_AFTER)
        await interaction.channel.purge(limit=100)

    @app_commands.command(name="del-message", description=app_commands.locale_str("del_msg_desc"))
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(amount=app_commands.locale_str("del_msg_amount_desc"))
    @app_commands.rename(amount=app_commands.locale_str("del_msg_amount"))
    async def delete_message(self, interaction: discord.Interaction, amount: int):
        if not await self._can_perform_in_channel(interaction, "text"):
            return

        assert isinstance(interaction.channel, discord.TextChannel)

        messages = [message async for message in interaction.channel.history(limit=amount if amount <= 100 else 100)]
        total_msg_find = len(messages)

        if total_msg_find == 0:
            await interaction.response.send_message("No messages have been deleted", ephemeral=True, delete_after=DELETE_AFTER)
            return

        await interaction.response.send_message(f"I will delete {total_msg_find} messages from this channel", ephemeral=True, delete_after=DELETE_AFTER)
        await interaction.channel.delete_messages(messages)


async def setup(bot: Grumpy) -> None:
    await bot.add_cog(Moderation(bot))