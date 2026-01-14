from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import Grumpy

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import get_current_time


class General(commands.Cog, name="general"):
    def __init__(self, bot: Grumpy) -> None:
        self.bot = bot
        """ self.context_menu_user = app_commands.ContextMenu(
            name=app_commands.locale_str("grab_id"), callback=self.grab_id
        ) """
        self.bot.tree.add_command(
            app_commands.ContextMenu(
                name=app_commands.locale_str("grab_id"), callback=self.grab_id
            )
        )
        self.bot.tree.add_command(
            app_commands.ContextMenu(
                name=app_commands.locale_str("report_message"), callback=self.report_message
            )
        )

    async def grab_id(self, interaction: discord.Interaction, user: discord.User) -> None:

        embed = discord.Embed(
            title=interaction.guild.name,
            description=f"The ID of {user.mention} is `{user.id}`",
            color=discord.Color.purple(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def report_message(self, interaction: discord.Interaction, message: discord.Message):
        if interaction.guild is None:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        await interaction.response.send_message(
            f"Thanks for reporting this message by {message.author.mention} to our moderators.", ephemeral=True
        )

    @app_commands.command(name="ping", description=app_commands.locale_str("ping_desc"))
    @app_commands.guild_only()
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

    @app_commands.command(name="help", description=app_commands.locale_str("help_desc"))
    @app_commands.guild_only()
    async def help(self, interaction: discord.Interaction):
        locale = interaction.locale
        embed_desc = await self.bot.get_command_translation("help_desc", locale)

        embed = discord.Embed(title = self.bot.user.name, description = embed_desc, color = 0xBEBEFE)

        for i in self.bot.cogs:
            if i == "owner" and not (await self.bot.is_owner(interaction.user)):
                continue

            cog = self.bot.get_cog(i.lower())
            if cog is None:
                continue

            data = []
            app_commands = cog.get_app_commands()
            for command in app_commands:
                description = await self.bot.get_command_translation(command.description, locale)
                data.append(f"/{command.name} - {description}")
            help_text = "\n".join(data)

            commands = cog.get_commands()
            for command in commands:
                description =  await self.bot.get_command_translation(command.description, locale)
                data.append(f"{self.bot.settings.command_prefix}{command.name} - {description}")
            help_text = "\n".join(data)

            embed.add_field(
                name=i.capitalize(), value=f"```{help_text}```", inline=False
            )
        embed.set_footer(text=f'Requested by {interaction.user.display_name} at {get_current_time()}', icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)


async def setup(bot: Grumpy) -> None:
    await bot.add_cog(General(bot))