from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import Grumpy

import discord
from discord.ext import commands


class General(commands.Cog, name="general"):
    def __init__(self, bot: Grumpy) -> None:
        self.bot = bot

    @commands.command(name="say")
    async def say(self, ctx: commands.Context, amount: int):
        print(amount)


async def setup(bot: Grumpy) -> None:
    await bot.add_cog(General(bot))