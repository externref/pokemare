from __future__ import annotations
from unittest.mock import NonCallableMagicMock


import disnake
from disnake.ext import commands

from core.bot import PokeMare


class General(commands.Cog):
    def __init__(self, bot: PokeMare) -> None:
        self.bot = bot

    @commands.slash_command(
        name="profile", description="Your profile connected with this bot."
    )
    async def profile(
        self, inter: disnake.AppCommandInteraction, user: disnake.User = None
    ) -> None:
        user = user or inter.user
        embed = (
            disnake.Embed(
                description=f"""
Balance: `{await self.bot.currency_db.get_coins_for(user.id)}` {self.bot.get_emoji(941929762912342027)}
Guess the Pokemon Guesses: `{await self.bot.gtp_db.get_guesses_for_user(user)}`
            """,
                color=disnake.Color.random(),
            )
            .set_author(name=user.name)
            .set_thumbnail(url=user.display_avatar.url)
        )
        await inter.send(embed=embed)


def setup(bot: PokeMare):
    bot.add_cog(General(bot))
