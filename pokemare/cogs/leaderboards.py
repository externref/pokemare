import disnake
from disnake.ext import commands

from ..bot import PokeMare


class Leaderboard(commands.Cog):
    def __init__(self, bot: PokeMare) -> None:
        self.bot = bot
        super().__init__()

    @commands.slash_command(
        name="leaderboard", description="Check various leaderboards in the bot"
    )
    async def lb_cmd(
        self, interaction: disnake.AppCommandInteraction, lb_type: str
    ) -> None:
        if lb_type == "guess the pokemon global":
            data = (await self.bot.gtp_db.global_leaderboard())[:10]
            embed = disnake.Embed(
                description="Showing top 10 users.", color=disnake.Color.purple()
            ).set_author(
                name="GLOBAL LEADERBOARD", icon_url=self.bot.user.display_avatar
            )
            embed.add_field(
                name="User",
                value="\n".join(
                    f"{str(i[0])}. `{i[1][0].__str__()}`"
                    for i in enumerate(data, start=1)
                ),
            )
            embed.add_field(
                name="Guesses", value="\n".join(i[1].__str__() for i in data)
            )

        await interaction.send(embed=embed)

    @lb_cmd.autocomplete("lb_type")
    async def lb_type_ac(self, inter: disnake.AppCommandInter, string: str) -> None:
        all = ["guess the pokemon global", "me"]
        if not string:
            return all
        return [a for a in all if a.lower().startswith(string)]


def setup(bot: PokeMare) -> None:
    bot.add_cog(Leaderboard(bot))
