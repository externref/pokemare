import disnake
from disnake.ext import commands

from core.bot import PokeMare


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
        badges = {
            1: self.bot.get_emoji(986111353083293696),
            2: self.bot.get_emoji(986111367452971008),
            3: self.bot.get_emoji(986111389376589844),
        }
        if lb_type == "whos that pokemon global":
            data_ = await self.bot.gtp_db.global_leaderboard()
            data = data_[:10]
            pos = 0
            for u in data_:
                pos += 1
                if u[0] == interaction.user:
                    break
            embed = (
                disnake.Embed(
                    description=f"Displaying top 10 global trainers.\n\nYou are ranked `#{pos}` with `{await self.bot.gtp_db.get_guesses_for_user(interaction.user)}` correct guesses.",
                    color=disnake.Color.purple(),
                )
                .set_author(
                    name="GLOBAL LEADERBOARD", icon_url=self.bot.user.display_avatar
                )
                .set_thumbnail(
                    url=badges.get(pos, self.bot.get_emoji(986110723597950996)).url
                )
                .set_footer(text="Use /profile to see your stats.")
            )
            embed.add_field(
                name=f"{self.bot.get_emoji(937618424169914398)} Trainers",
                value="\n".join(
                    f"{badges.get(i[0],self.bot.get_emoji(986110723597950996))}. `{i[1][0].__str__()}`"
                    for i in enumerate(data, start=1)
                ),
            )

            def make_string(g: int) -> None:
                return "`💠 " + ("0" * len(str(10000 // g))) + str(g) + "`"

            embed.add_field(
                name="❔ Guesses", value="\n".join(make_string(i[1]) for i in data)
            )

        await interaction.send(embed=embed)

    @lb_cmd.autocomplete("lb_type")
    async def lb_type_ac(self, inter: disnake.AppCommandInter, string: str) -> None:
        all = ["whos that pokemon global"]
        if not string:
            return all
        return [a for a in all if a.lower().startswith(string)]


def setup(bot: PokeMare) -> None:
    bot.add_cog(Leaderboard(bot))
