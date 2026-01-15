from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Literal

if TYPE_CHECKING:
    from ..bot import Grumpy

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import get_current_time


async def is_owner(interaction: discord.Interaction):
    assert isinstance(interaction.client, commands.Bot)

    if not await interaction.client.is_owner(interaction.user):
        return False
    return True


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot: Grumpy) -> None:
        self.bot = bot

    def _create_embed(self, message: str, success: bool) -> discord.Embed:
        return discord.Embed(
            title="Owner action:",
            description=message,
            color=discord.Color.purple() if success else discord.Color.red()
        )

    async def _send_ctx_embed(self, ctx: commands.Context, message: str, success: bool = True) -> None:
        embed = self._create_embed(message, success)
        embed.set_footer(text=f'Requested by {ctx.author.display_name} at {get_current_time()}', icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed, ephemeral=True)

    def _is_valid_scope(self, scope: str) -> bool:
        return scope in ["global", "guild", "dev"]

    async def _sync_guild_commands(self, ctx: commands.Context, guild: discord.Guild, message: str):
        await ctx.send(message)

        try:
            self.bot.tree.copy_global_to(guild=guild)
            await self.bot.tree.sync(guild=guild)
        except discord.HTTPException as exc:
            response = f"Slash Command synchronization failed in `{guild.name}`"
            await self._send_ctx_embed(ctx, response, False)
            self.bot.logger.error(response, exc_info=exc)
            return

        response = f"Slash commands have been successfully synchronized in `{guild.name}`"
        await self._send_ctx_embed(ctx, response)
        self.bot.logger.info(response)

    async def _unsync_guild_commands(self, ctx: commands.Context, guild: discord.Guild, message: str):
        await ctx.send(message)

        try:
            self.bot.tree.clear_commands(guild=guild, type=None)
            await self.bot.tree.sync(guild=guild)
        except discord.HTTPException as exc:
            response = f"Slash Command synchronization failed in `{guild.name}`"
            await self._send_ctx_embed(ctx, response, False)
            self.bot.logger.error(response, exc_info=exc)
            return

        response = f"Slash commands have been successfully unsynchronized in `{guild.name}` with success"
        await self._send_ctx_embed(ctx, response)
        self.bot.logger.info(response)

    @commands.command(description="Shut down the bot", aliases=["off"])
    @commands.is_owner()
    async def shutdown(self, ctx: commands.Context) -> None:
        await ctx.message.delete()

        await self._send_ctx_embed(ctx, "Shutting down... Bye! :wave:", True)

        await self.bot.change_presence(status=discord.Status.offline)
        await self.bot.close()

    @commands.command(name="sync", description="Synchronizes the slash commands")
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, scope: str, guild_id: Optional[int] = None) -> None:
        await ctx.message.delete()

        if not self._is_valid_scope(scope):
            await self._send_ctx_embed(ctx, "The response can only be `global`, `guild` or `dev`", False)
            return

        if scope == "global":
            await ctx.send("Slash commands will be globally synchronized.")

            try:
                await self.bot.tree.sync()
            except discord.HTTPException as exc:
                log_msg ="Global command synchronization has failed"
                await self._send_ctx_embed(ctx, log_msg, False)
                self.bot.logger.error(log_msg, exc_info=exc)
                return

            log_msg = "Slash commands are synchronized globally (may take some time)."
            await self._send_ctx_embed(ctx, log_msg)
            self.bot.logger.info(log_msg)
            return

        if scope == "guild":
            assert isinstance(ctx.guild, discord.Guild)

            if guild_id:
                guild = self.bot.get_guild(guild_id)

                if guild is None:
                    await self._send_ctx_embed(ctx, "Sorry, I am not in this guild.", False)
                    return

                await self._sync_guild_commands(ctx, ctx.guild, f"Slash commands will be synchronized in `{guild.name}`.")
                return

            if guild_id is None:
                await self._sync_guild_commands(ctx, ctx.guild, "Slash commands will be synchronized in this guild.")
                return

        if scope == "dev":
            test_guild_id = self.bot.settings.test_guild_id

            if test_guild_id is None:
                await self._send_ctx_embed(ctx, "No development server ID has been defined in the environment variables file.", False)
                return

            guild = self.bot.get_guild(test_guild_id)
            if guild is None:
                await self._send_ctx_embed(ctx, "Dude, why am I not on your fucking development Discord server?", False)
                return

            await self._sync_guild_commands(ctx, guild, f"Slash commands will be synchronized in the test server `{guild.name}`.")

    @commands.command(name="unsync", description="Unsynchronizes the slash commands")
    @commands.is_owner()
    async def unsync(self, ctx: commands.Context, scope: str, guild_id: Optional[int] = None) -> None:
        await ctx.message.delete()

        if not self._is_valid_scope(scope):
            await self._send_ctx_embed(ctx, "The response can only be `global`, `guild` or `dev`", False)
            return

        if scope == "global":
            await ctx.send("Slash commands will be globally unsynchronized.")

            try:
                self.bot.tree.clear_commands(guild=None, type=None)
                await self.bot.tree.sync(guild=None)
            except discord.HTTPException as exc:
                log_msg ="Global command unsynchronization has failed"
                await self._send_ctx_embed(ctx, log_msg, False)
                self.bot.logger.error(log_msg, exc_info=exc)
                return

            log_msg = "Slash commands are synchronized globally (may take some time)."
            await self._send_ctx_embed(ctx, log_msg)
            self.bot.logger.info(log_msg)
            return

        if scope == "guild":
            assert isinstance(ctx.guild, discord.Guild)

            if guild_id:
                guild = self.bot.get_guild(guild_id)

                if guild is None:
                    await self._send_ctx_embed(ctx, "Sorry, I am not in this guild.", False)
                    return

                await self._unsync_guild_commands(ctx, ctx.guild, f"Slash commands will be unsynchronized in `{guild.name}`.")
                return

            if guild_id is None:
                await self._unsync_guild_commands(ctx, ctx.guild, "Slash commands will be unsynchronized in this guild.")
                return

        if scope == "dev":
            test_guild_id = self.bot.settings.test_guild_id

            if test_guild_id is None:
                await self._send_ctx_embed(ctx, "No development server ID has been defined in the environment variables file.", False)
                return

            guild = self.bot.get_guild(test_guild_id)
            if guild is None:
                await self._send_ctx_embed(ctx, "Dude, why am I not on your fucking development Discord server?", False)
                return

            await self._unsync_guild_commands(ctx, guild, f"Slash commands will be unsynchronized in the test server `{guild.name}`.")

    async def cog_command_error(self, ctx: commands.Context, error: Exception) -> None:
        if isinstance(error, commands.errors.NotOwner):
            await ctx.send(f"{ctx.author.mention} nothing to see here my friend.", ephemeral=True)

            if ctx.guild:
                self.bot.logger.warning(
                    f"{ctx.author} (ID: {ctx.author.id}) tried to execute an owner only command in the guild {ctx.guild.name} (ID: {ctx.guild.id}), but the user is not an owner of the bot."
                )
            else:
                self.bot.logger.warning(
                    f"{ctx.author} (ID: {ctx.author.id}) tried to execute an owner only command in the bot's DMs, but the user is not an owner of the bot."
                )

            return

        # print("An error occurred in the Owner cog from COMMAND: '%s' - ERROR: '%s %s'", ctx.invoked_with.upper(), error, type(error))
        self.bot.logger.error("An error occurred in the Owner cog from COMMAND: '%s' - ERROR: '%s %s'", ctx.invoked_with.upper(), error, type(error))


async def setup(bot: Grumpy) -> None:
    await bot.add_cog(Owner(bot))