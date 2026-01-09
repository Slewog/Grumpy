from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import Grumpy

import discord
from discord.ext import commands


class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot: Grumpy) -> None:
        self.bot = bot


async def setup(bot: Grumpy) -> None:
    await bot.add_cog(Moderation(bot))