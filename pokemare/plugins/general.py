from __future__ import annotations

from datetime import datetime

from discord.embeds import Embed
from discord.ext.commands.cog import Cog
from discord.ext.commands.context import Context
from discord.ext.commands.core import command, has_permissions

from ..bot import PokeMare


class General(Cog):
    """General Bot commands"""

    def __init__(self, bot: PokeMare) -> None:
        self.bot = bot
        self.last_loaded = datetime.now()

    @command(name="ping", description="Bot Latency", aliases=["latency", "pong"])
    async def _ping(self, context: Context) -> None:
        """Ping Pong"""
        await context.reply(embed=Embed(description=f"Ping : `{round(self.bot.latency, 2)} ms`",color=self.bot.color))

def setup(bot: PokeMare) -> None:
    bot.add_cog(General(bot))
