import aiohttp
from io import BytesIO
from typing import Union, Optional

from disnake.user import User
from disnake.file import File
from disnake.colour import Color
from disnake.embeds import Embed
from disnake.message import Message
from disnake.ext.commands.cog import Cog
from disnake.interactions import AppCmdInter
from disnake.ext.commands.core import command
from disnake.ext.commands.context import Context
from disnake.ext.commands.slash_core import slash_command, Option, OptionType

from PIL import Image, ImageDraw, ImageFont


from .. import PokeMare


class InventoryInfo(Cog, name="Tools"):
    """Tools to get info about Pokemons and items"""

    def __init__(self, bot: PokeMare):
        self.hidden = False
        self.emoji = "<:pokedex:937676313764982814>"
        self.bot = bot

    @slash_command(
        name="profile",
        description="Profile of an user",
        options=[
            Option(
                name="user",
                description="User to see profile of",
                required=False,
                type=OptionType.user,
            )
        ],
    )
    async def see_profile(self, interaction: AppCmdInter, user: User = None) -> None:
        await interaction.response.defer()
        user = user or interaction.author
        data = await self.bot.user_database.get_user_information(user.id)
        if not data:
            return await interaction.edit_original_message(
                "The user has not started their journey yet.", ephemeral=True
            )
        bg_image = Image.open("images/card_bg.png")
        user_avatar = Image.open(BytesIO(await user.display_avatar.read())).resize(
            (225, 225)
        )
        bg_image.paste(user_avatar, ((520, 112)))
        draw = ImageDraw.Draw(bg_image)
        draw.text(
            (55, 88),
            interaction.author.name,
            font=ImageFont.truetype("data/profile_font.ttf", 42),
            fill=(189, 201, 193),
        )
        draw.text(
            (40, 200),
            f"Pokédollars : {data[3]}",
            font=ImageFont.truetype("data/profile_font.ttf", 42),
            fill=(189, 201, 193),
        )
        draw.text(
            (40, 250),
            f"Star Fragements : {data[4]}",
            font=ImageFont.truetype("data/profile_font.ttf", 42),
            fill=(189, 201, 193),
        )
        bg_image.save(f"trash/{interaction.author.id}.png")
        embed = Embed(color=self.bot.color)
        embed.set_image(file=File(f"trash/{interaction.author.id}.png"))
        embed.set_author(name=user.name, icon_url=user.display_avatar)
        await interaction.edit_original_message(embed=embed)

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
            if int(data["id"]) > 151:
                return await ctx.reply(
                    embed=Embed(
                        color=Color.red(),
                        title="Pokédex",
                        description=f"`{pokemon}` is not a valid Pokémon name/id\n**NOTE** : The Pokédex includes Pokémons only from kanto! ",
                    ).set_thumbnail(
                        url="https://cdn.discordapp.com/emojis/872786088480100373.webp"
                    )
                )
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
                "Evolution Line": " , ".join(set(data2["family"]["evolutionLine"]))
                or "No evolutions",
                "Abilities": " , ".join(data2["abilities"]),
                "Stats": " , ".join(
                    f"{key} - {value}" for key, value in (data2["stats"]).items()
                ).title(),
                "Genders": " , ".join(data2["gender"])
                .replace("female", "♀️")
                .replace("male", "♂️"),
                "Egg Group": " , ".join(data2["egg_groups"]),
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

    @command(
        name="move",
        aliases=["moveinfo"],
        description="Info about the mentioned move name/ID",
    )
    async def move_info(self, ctx: Context, *, move) -> Optional[Message]:
        """Move info"""
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://pokeapi.co/api/v2/move/{move.replace(' ','-')}"
            )
            if (await response.text()).lower() == "not found":
                return await ctx.reply(
                    embed=Embed(
                        color=Color.red(),
                        title="Pokédex",
                        description=f"`{move}` is not a valid Move name/id",
                    ).set_thumbnail(
                        url="https://cdn.discordapp.com/emojis/872786088480100373.webp"
                    )
                )
        data = await response.json()
        description = {
            "Accuracy": data["accuracy"],
            "Effect Chance": data["effect_chance"],
            "PP": data["pp"],
            "Power": data["power"],
            "Priority": data["priority"],
            "Damage Class": (data["damage_class"]["name"]),
            "From Generation": data["generation"]["name"],
            "Effects": " , ".join(
                d["short_effect"].replace("$effect_chance", str(data["effect_chance"]))
                for d in (data["effect_entries"])
            ),
        }
        embed = Embed(
            color=Color.red(),
            description="\n".join(
                f"**{key} :** {item}" for key, item in description.items()
            ),
        )
        embed.set_author(
            icon_url="https://cdn.discordapp.com/emojis/872786088480100373.webp",
            name=data["name"].upper() + " #" + str(data["id"]),
        )
        await ctx.reply(embed=embed)


def setup(bot: PokeMare):
    bot.add_cog(InventoryInfo(bot))
