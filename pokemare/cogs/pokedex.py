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
            response = await session.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
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
            description = {
                "ID": data2["id"],
                "Type": " , ".join(data2["type"]),
                "Height": data2["height"],
                "Weight": data2["weight"],
                "Evolution Line": " , ".join(data2["family"]["evolutionLine"]),
                "Abilities" : " , ".join(data2["abilities"]),
                "Genders": " , ".join(data2["gender"]),
            }

            embed = Embed(
                color=Color.red(),
                description=data2["description"]
                + "\n\n"
                + "\n".join(f"**{key} :** {item}" for key, item in description.items()),
            ).set_thumbnail(
                url=data2["sprites"]["animated"]
            )
            embed.set_author(
                icon_url="https://cdn.discordapp.com/emojis/872786088480100373.webp",
                name=data["name"].upper(),
            )
            await ctx.reply(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Pokedex(bot))
