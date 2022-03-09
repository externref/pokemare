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
        await context.reply(
            embed=Embed(
                description=f"Ping : `{round(self.bot.latency, 2)} ms`",
                color=self.bot.color,
            )
        )

    @command(
        name="prefix", description="Change prefix for the server", aliases=["setprefix"]
    )
    @has_permissions(manage_guild=True)
    async def _set_prefix(self, context: Context, new_prefix: str) -> None:
        """Change Prefix"""
        if any(
            invalid_char
            for invalid_char in new_prefix
            if invalid_char in ("@", "#", "\\", "`")
        ):
            return await context.reply(
                embed=Embed(
                    description="Prefix cannot have these elements : '@' , '#' , '', '`",
                    color=self.bot.color,
                )
            )
        await self.bot.prefix_database.set_prefix(context, new_prefix)
        await context.send(
            embed=Embed(
                description=f"Changed prefix to `{new_prefix}`", color=self.bot.color
            )
        )


def setup(bot: PokeMare) -> None:
    bot.add_cog(General(bot))
