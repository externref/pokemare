from __future__ import annotations

import random

import disnake
from disnake.ext import commands

from core.bot import PokeMare


class GTPObject:
    def __init__(self, bot, pokemon_id: int) -> None:
        self.bot: PokeMare = bot
        self.pokemon_id: int = pokemon_id

    @property
    def hidden_image(self) -> str:
        return f"https://raw.githubusercontent.com/PokeMare/resources/main/hidden_pokemons/{self.pokemon_id}.png"

    @property
    def revealed_image(self) -> disnake.File:
        return f"https://raw.githubusercontent.com/PokeMare/resources/main/revealed_pokemons/{self.pokemon_id}.png"


class Games(commands.Cog):
    def __init__(self, bot: PokeMare) -> None:
        self.bot = bot
        super().__init__()

    @commands.slash_command(
        name="guess_the_pokemon",
        description="Guess the correct pokemon to reach the leaderboard!",
    )
    @commands.cooldown(1, 20, type=commands.BucketType.user)
    async def gtp_command(self, interaction: disnake.AppCommandInter) -> None:
        p_id = random.randint(1, 151)
        gtp = GTPObject(self.bot, p_id)
        pokemon: dict | None = self.bot.pokemon_dict.get(str(p_id))
        pokemon_name = pokemon.get("name")
        pokemon_info = pokemon.get("description")

        hidden_embed = disnake.Embed(
            color=disnake.Color.yellow(),
            description="Respond with the name or the ID of the pokemon",
        ).set_author(name="Guess the Pokemon")
        hidden_embed.set_image(url=gtp.hidden_image)

        await interaction.send(embed=hidden_embed)
        revealed_embed = disnake.Embed(
            description=f"The pokemon was: ||{pokemon_name.title()}\n{pokemon_info}||"
        )
        revealed_embed.set_image(url=gtp.revealed_image)
        try:
            msg: disnake.Message = await self.bot.wait_for(
                "message",
                check=lambda m: m.author == interaction.user
                and m.channel == interaction.channel
                and m.content.lower() in (str(p_id), pokemon_name.lower()),
                timeout=30,
            )
        except:
            revealed_embed.color = disnake.Color.red()
            revealed_embed.set_footer(text="Better luck new time!")
            revealed_embed.title = "Oh no, wrong guess."
            await interaction.edit_original_message(embed=revealed_embed)

        await self.bot.gtp_db.add_guess(interaction.author)
        revealed_embed.color = disnake.Color.green()
        revealed_embed.set_footer(text="Use /leaderboard me to see your stats")
        revealed_embed.title = "Correct!"
        await interaction.edit_original_message(embed=revealed_embed)


def setup(bot: PokeMare) -> None:
    bot.add_cog(Games(bot))