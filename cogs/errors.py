from __future__ import annotations

import disnake
from disnake.ext import commands

from core.bot import PokeMare


class ErrorHandler(commands.Cog):
    def __init__(self, bot: PokeMare) -> None:
        self.bot = bot
        self.ignored = True

    @commands.Cog.listener()
    async def on_slash_command_error(
        self, inter: disnake.AppCommandInteraction, error: Exception
    ) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            await inter.send(
                embed=disnake.Embed(
                    description=f"You gotta wait for `{error.retry_after}` seconds to use this command again.",
                    color=disnake.Color.red(),
                )
            )
        else:
            raise error


def load(bot: PokeMare):
    bot.add_cog(ErrorHandler(bot))
