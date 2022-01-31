from typing import Union
import aiohttp
from disnake.ext.commands.bot import Bot
from disnake.ext.commands.cog import Cog
from disnake.ext.commands.core import command
from disnake.ext.commands.context import Context
from disnake.embeds import Embed
from disnake.colour import Color


class Pokedex(Cog, name="Pokedex"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="pokedex",
        description="Lookup for a pokemon in the pokedex",
        aliases=["dex"],
    )
    async def pokedex(self, ctx: Context, *, pokemon: str):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"
            )
            if (await response.text()).lower() == "not found":
                return await ctx.reply(
                    embed=Embed(
                        color=Color.red(),
                        title="Pokédex",
                        description=f"`{pokemon}` is not a valid Pokémon name/id\n**NOTE** : The Pokédex includes Pokémons only from kanto! ",
                    ).set_thumbnail(
                        url="https://cdn.discordapp.com/emojis/872786088480100373.webp"
                    )
                )
            data = await response.json()
            response2 = await session.get(
                f"https://some-random-api.ml/pokedex?pokemon={data['name']}"
            )

            data2 = await response2.json()
            emojis = " , ".join(
                [
                    str(emoji) + " " + emoji.name.title()
                    for emoji in ctx.bot.get_guild(862240879339241493).emojis
                    if emoji.name.lower() in " , ".join(data2["type"]).lower()
                ]
            )
            description = {
                "Type": emojis or " , ".join(data2["type"]),
                "Height": data2["height"],
                "Weight": data2["weight"],
                "Evolution Line": " , ".join(data2["family"]["evolutionLine"])
                or "No evolutions",
                "Abilities": " , ".join(data2["abilities"]),
                "Genders": " , ".join(data2["gender"]),
            }

            embed = Embed(
                color=Color.red(),
                description="*"
                + data2["description"]
                + "*\n\n"
                + "\n".join(f"**{key} :** {item}" for key, item in description.items()),
            ).set_thumbnail(url=data2["sprites"]["animated"])
            # ).set_thumbnail(url=data['sprites']['versions']['generation-iii']['firered-leafgreen']['front_default'])
            embed.set_author(
                icon_url="https://cdn.discordapp.com/emojis/872786088480100373.webp",
                name=data["name"].upper() + " #" + data2["id"],
            )
            await ctx.reply(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Pokedex(bot))
