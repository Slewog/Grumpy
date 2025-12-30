import discord
from discord.ext import commands
from discord import app_commands

class OwnerCog(commands.Cog):
    """Cog for owner-only commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    """ @app_commands.command(name="shutdown", description="Shut down the bot.")
    @app_commands.checks.is_owner()
    async def shutdown(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Shutting down...")
        await self.bot.close() """


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OwnerCog(bot))