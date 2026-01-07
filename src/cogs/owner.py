import discord
from logging import getLogger
from discord.ext import commands
from discord import app_commands
from typing import TYPE_CHECKING, Optional, Literal

from src.utils import get_current_time

if TYPE_CHECKING:
    from src.bot import Grumpy


async def is_owner(interaction: discord.Interaction):
    if not await interaction.client.is_owner(interaction.user):
        return False
    return True


class Owner(commands.Cog, name="Owner"):
    """Cog for owner-only commands."""

    def __init__(self, bot: Grumpy) -> None:
        self.bot = bot

    async def _sync_commands(self, guild: discord.Guild, ctx: commands.Context) -> None:
        try:
            self.bot.tree.copy_global_to(guild=guild)
            await self.bot.tree.sync(guild=guild)
        except discord.HTTPException as exc:
            self.bot.log(f"Slash Command synchronization failed in `{guild.name}`", level="ERROR", exc_info=exc)
            await self._send_ctx_embed(ctx,
                f"Slash Command synchronization failed in `{guild.name}`."
            )
            return

        self.bot.log("Slash Commands synchronized in %s with sucess", guild.name)
        await self._send_ctx_embed(ctx,
            f"Slash commands have been synchronized in `{guild.name}`."
        )

    async def _unsync_commands(self, guild: discord.Guild, ctx: commands.Context) -> None:
        try:
            self.bot.tree.clear_commands(guild=guild, type=None)
            await self.bot.tree.sync(guild=guild)
        except discord.HTTPException as exc:
            self.bot.log(f"Slash Command synchronization failed in `{guild.name}`", level="ERROR", exc_info=exc)
            await self._send_ctx_embed(ctx,
               f"Slash Command unsynchronization failed in `{guild.name}`."
            )
            return

        self.bot.log("Slash Commands have been unsynchronized in %s with sucess", guild.name)
        await self._send_ctx_embed(ctx,
            f"Slash commands have been unsynchronized in `{guild.name}` with success."
        )

    async def _valid_guild_id(self, guild_id: str, ctx: commands.Context) -> int | Literal[False]:
        if guild_id is None:
            await ctx.send("To synchronize/unsynchronize commands within a guild, I need its ID.")
            return False

        try:
            valid_id = int(guild_id)
        except:
            await ctx.send("this guild id is invalid")
            return False

        return valid_id

    def _is_valid_scope(self, scope: str) -> bool:
        return scope in ["global", "guild", "dev"]

    def _get_embed(self, message: str)  -> discord.Embed:
        return discord.Embed(
            title="Owner action:",
            description=message,
            color=discord.Color.purple(), # 0xBEBEFE
        )

    async def _send_ctx_embed(self, ctx: commands.Context, message: str) -> None:
        embed = self._get_embed(message)
        embed.set_footer(text=f'Requested by {ctx.author.display_name} at {get_current_time()}', icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    async def _send_interaction_embed(self, interaction: discord.Interaction, message: str) -> None:
        embed = self._get_embed(message)
        embed.set_footer(text=f'Requested by {interaction.user.display_name} at {get_current_time()}', icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="shutdown", description="Shut down the bot.")
    @app_commands.check(is_owner)
    async def shutdown(self, interaction: discord.Interaction) -> None:
        await self._send_interaction_embed(interaction, "Shutting down... Bye! :wave:")

        await self.bot.change_presence(status=discord.Status.offline)
        await self.bot.close()

    @commands.command(name="sync", description="Synchonizes the slash commands.")
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, scope: str, guild_id: Optional[str] = None) -> None:
        if not self._is_valid_scope(scope):
            await ctx.send("The response can only be `global`, `guild` or `dev`")
            return

        if scope == "global":
            await ctx.send("Slash commands will be globally synchronized.")

            try:
                await self.bot.tree.sync()
            except discord.HTTPException:
                self.bot.log("Global command synchronization failed", level="ERROR")
                await self._send_ctx_embed(ctx,
                    "Global command synchronization failed"
                )

            self.bot.log("Slash commands are synchronized globally (may take some time).")
            await self._send_ctx_embed(ctx,
                "Slash commands are synchronized globally (may take some time)."
            )
            return

        if scope == "guild":
            id = await self._valid_guild_id(guild_id, ctx)
            if not id:
                return

            guild = self.bot.get_guild(id)
            if guild is None: 
                await ctx.send("I am not in this guild.")
                return

            await ctx.send(f"Slash commands will be synchronized in the server `{guild.name}`.")

            await self._sync_commands(guild, ctx)
            return

        if scope == "dev":
            test_guild_id = self.bot.get_test_guild_id()

            if test_guild_id is None:
                await ctx.send("No development server ID has been defined in the variable file.")
                return

            guild = self.bot.get_guild(test_guild_id)
            if guild is None: 
                await ctx.send("Dude, why am I not on your fucking development Discord server?")
                return

            await ctx.send(f"Slash commands will be synchronized in the server `{guild.name}`.")

            await self._sync_commands(guild, ctx)

    @commands.command(name="unsync", description="Unsynchonizes the slash commands.")
    @commands.is_owner()
    async def unsync(self, ctx: commands.Context, scope: str, guild_id: Optional[str] = None) -> None:
        if not self._is_valid_scope(scope):
            await ctx.send("The response can only be `global`, `guild` or `dev`", ephemeral=True)
            return

        if scope == "global":
            await ctx.send("Slash commands will be globally unsynchronized.")

            self.bot.tree.clear_commands(guild=None, type=None)
            await self.bot.tree.sync(guild=None)
            await self._send_ctx_embed(ctx,
                "Slash commands have been globally unsynchronized.(may take some time)."
            )
            return

        if scope == "guild":
            id = await self._valid_guild_id(guild_id, ctx)
            if not id:
                return

            guild = self.bot.get_guild(id)
            if guild is None: 
                await ctx.send("I am not in this guild.")
                return

            await ctx.send(f"Slash commands will be unsynchronized in the server `{guild.name}`.")

            await self._unsync_commands(guild, ctx)

        if scope == "dev":
            test_guild_id = self.bot.get_test_guild_id()

            if test_guild_id is None:
                await ctx.send("No development server ID has been defined in the variable file.", ephemeral=True)
                return

            guild = self.bot.get_guild(test_guild_id)

            if guild is None: 
                await ctx.send("Dude, why am I not on your fucking development Discord server?", ephemeral=True)
                return

            await ctx.send(f"Slash commands will be unsynchronized in the server `{guild.name}`.")

            await self._unsync_commands(guild, ctx)

    async def cog_app_command_error(self, interaction: discord.Interaction, error: Exception) -> None:
        cmd = interaction.command

        if isinstance(error, discord.app_commands.errors.CheckFailure):
            await interaction.response.send_message("Nothing to see here my friend.", ephemeral=True)
            return

        # print(f'An error occurred in the Onwer cog !\n- Slash Command: {cmd.name}\n- Error: {error} ({type(error)})')
        self.bot.log("An error occurred in the Owner cog from SLASH COMMAND: '%s' - ERROR: '%s %s'", cmd.name, error, type(error))

    async def cog_command_error(self, ctx: commands.Context, error: Exception) -> None:
        if isinstance(error, commands.errors.NotOwner):
            await ctx.send(f"{ctx.author.mention} nothing to see here my friend.", ephemeral=True)
            return

        # print("An error occurred in the Owner cog from COMMAND: '%s' - ERROR: '%s %s'", ctx.invoked_with.upper(), error, type(error))
        self.bot.log("An error occurred in the Owner cog from COMMAND: '%s' - ERROR: '%s %s'", ctx.invoked_with.upper(), error, type(error))